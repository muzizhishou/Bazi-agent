import os
from pathlib import Path
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from Bazi_calculate import calculate_bazi
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents.structured_output import ToolStrategy
import shutil

# 十个天干各自对应的五行属性和阴阳属性,这是命理学里固定不变的基础数据
STEM_INFO = {
    "甲": ("木", "阳"), "乙": ("木", "阴"),
    "丙": ("火", "阳"), "丁": ("火", "阴"),
    "戊": ("土", "阳"), "己": ("土", "阴"),
    "庚": ("金", "阳"), "辛": ("金", "阴"),
    "壬": ("水", "阳"), "癸": ("水", "阴"),
}

# 五行"相生"关系:木生火,火生土,土生金,金生水,水生木
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}

# 五行"相克"关系:木克土,土克水,水克火,火克金,金克木
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# 日主天干 → 人格原型的"底色"命名
# 这是产品设计层面的固定表,不会因为LLM每次生成而变化,
# 保证"同一个日主天干"永远对应同一个原型名字(类似MBTI的16型名称固定不变)
ARCHETYPE_BASE = {
    # 木:向上生长的画面感
    "甲": "拔地苍木",     # 保留,你认可的
    "乙": "捕风柔藤",     # 藤蔓在风里摇曳,柔韧又有动态,画面清晰

    # 火:光与热的画面感
    "丙": "赤霄烈阳",     # 保留,你认可的
    "丁": "灯花烛影",     # 黑夜里一豆烛光,微弱但存在感强,画面直接

    # 土:承载/厚重的画面感
    "戊": "横断厚岭",     # 一座横亘的山岭,扎实、有分量,一读就懂
    "己": "沃土育禾",     # 田地里长着庄稼,滋养、包容,画面朴素但清晰

    # 金:锋利/贵重的画面感
    "庚": "出鞘寒锋",     # 刀剑出鞘的那一瞬间,锐利、有张力
    "辛": "掌心藏玉",     # 手心里握着一块玉,精致、私密、被珍视的画面感

    # 水:流动/辽阔的画面感
    "壬": "奔流湖海",     # 江河汇入大海,辽阔又有力量,直白但有气势
    "癸": "空山烟雨",     # 屋檐下滴落的细雨,安静、绵密,画面很具体
}
# 十神 → 修饰性人格标签
# 同样是固定表,用来给"底色"加上更具体的行为/气质修饰
TEN_GOD_MODIFIER = {
    "比肩": "孤峰独行客",     # 比肩=独立自主,"孤峰"强化那种"不需要陪伴也自洽"的意象
    "劫财": "逐浪结义人",     # 劫财=豪爽social,"逐浪"有动感,"结义"点出重情义
    "食神": "闲云煮茶者",     # 食神=温和享受型,"闲云煮茶"是很标准的东方松弛感意象
    "伤官": "锋芒未定型",     # 伤官=才华与叛逆,"未定型"暗示还在生长、不被定义
    "正财": "细水长流者",     # 正财=稳定踏实,"细水长流"精准对应其务实但不失温度
    "偏财": "游川拾贝人",     # 偏财=机缘意外之财,"游川拾贝"有随性捕捉机会的画面感
    "正官": "执灯守则者",     # 正官=规则与领导,"执灯"比"守护"更有主动引领的意味
    "偏官": "破晓踏浪者",     # 偏官=魄力与开拓,"破晓"取其冲破黑暗、率先行动之意
    "正印": "怀光护雏人",     # 正印=庇护与学识,"怀光"比"庇护"更温柔且有画面
    "偏印": "掌灯窥微者",     # 偏印=洞察与幕后,"掌灯窥微"呼应其精明缜密的特质
}

# ========== 第一步:把排盘计算函数,包装成Agent能识别、能调用的"工具" ==========
@tool
def bazi_calculator_tool(year:int,month:int,day:int,hour:int) ->str:
    """
    根据用户提供的阳历(公历)出生年、月、日、时(24小时制),
    计算出准确的生辰八字排盘,包括年柱、月柱、日柱、时柱。

    在需要给用户做八字命理分析之前,必须先调用这个工具获取准确的排盘结果,
    不要凭自己的知识直接猜测或编造排盘内容,因为排盘计算是有严格规则的,
    必须依赖精确计算,不能靠语言模型自己推算。
    """
    # 调用之前写好、已经验证过的计算函数
    result = calculate_bazi(year, month, day, hour)
    # 因为工具的返回值最终要被"喂回"给LLM看,LLM只能理解文字,
    # 所以这里把字典格式化成一段清晰的文字,而不是直接返回Python字典
    formatted_result = (
        f"年柱: {result['年柱']}, "
        f"月柱: {result['月柱']}, "
        f"日柱: {result['日柱']}, "
        f"时柱: {result['时柱']}"
    )

    return formatted_result

class BaziAnalysis(BaseModel):
    year_pillar: str = Field(description="年柱")
    month_pillar: str = Field(description="月柱")
    day_pillar: str = Field(description="日柱")
    hour_pillar: str = Field(description="时柱")

    archetype_title: str = Field(description="人格原型称号,必须是调用archetype_naming_tool得到的原始结果,不允许自己改写或美化")

    shareable_tagline: str = Field(description="一句话slogan,20字以内,风格参考小红书人格测试文案,要有记忆点或反差感,适合配图分享")

    personality_summary: str = Field(description="人格解读正文,80-120字,现代白话文,句子简短克制,不用文言腔调,不出现任何命理术语(年柱/月柱/日坐/月令等禁用),避免网络热梗和调侃句式")

    traits: list[str] = Field(description="5-6条具体特质,每条不超过18字,现代口语但不浮夸,不用'你是那种...'这类套话句式,不出现命理术语")

def build_wuxing_dict(docs: list[Document]) -> dict:
    """
    把知识库文档列表,转换成一个"单字符号 -> 解释内容"的字典,方便精确查找。
    天干地支类词条(如"丙火""亥水")用首字("丙""亥")作为额外的查找key,
    因为排盘结果给出的往往是单字,不是"丙火"这种完整两字词。
    十神类词条(如"比肩""正财")本身就是固定的两字词,不需要拆分,直接用完整词作为key。
    """
    wuxing_suffixes = {"金", "木", "水", "火", "土"}  # 五行后缀,用来判断是不是"干支+五行"这种格式
    d = {}

    for doc in docs:
        topic = doc.metadata.get("topic", "").strip()
        if not topic:
            continue

        # 完整词本身也存一份,保证"丙火"这种完整查询也能命中
        d[topic] = doc.page_content

        # 如果是"干支+五行"这种两字格式(比如"丙火"),额外用第一个字("丙")建一个索引
        if len(topic) == 2 and topic[-1] in wuxing_suffixes:
            d[topic[0]] = doc.page_content

    return d



@tool
def wuxing_knowledge_tool(query: str) -> str:
    """
    查询五行(如丙火、戊土)或者天干地支相关的传统命理知识解释。
    当你需要了解某个具体的天干或地支(比如丙、戌、乙、未等)代表的性格含义时,
    调用这个工具,输入你想查询的天干或地支名称,可以是单字(如"辛"),
    也可以是完整的柱名(如"辛亥"),工具会自动拆解查找。
    """
    query = query.strip()

    # 第一步:整体精确匹配(比如查询本身就是"丙火"或者单字"丙")
    if query in wuxing_dict:
        return wuxing_dict[query]

    # 第二步:如果整体没找到,尝试把query当作"复合词"(比如"辛亥"),
    # 逐个检查字典里的"单字key"是否出现在这个复合词里
    matches = []
    for key, content in wuxing_dict.items():
        # 只用"单字"的key做这种拆解匹配,避免"辛金"这种两字key也被误判成子串
        if len(key) == 1 and key in query:
            matches.append(content)

    if matches:
        # 用集合去重,防止同一条内容因为字符重复被匹配两次
        return "\n".join(dict.fromkeys(matches))

    # 第三步:实在找不到,才退回到语义检索兜底
    docs = wuxing_retriever.invoke(query)
    if not docs:
        return "未找到相关的命理知识解释。"
    return "\n".join([doc.page_content for doc in docs])
    # 第二步:如果精确匹配没找到,再退化到语义检索,作为兜底
    docs = wuxing_retriever.invoke(query)
    if not docs:
        return "未找到相关的命理知识解释。"
    result_text = "\n".join([doc.page_content for doc in docs])
    return result_text

def get_ten_god(day_stem: str, target_stem: str) -> str:
    """
    根据"日主天干"和"目标天干",按照五行生克规则,计算出对应的十神名称。
    十神的判定规则(基于日主和目标天干的五行关系 + 阴阳是否相同):
    - 五行相同 → 比肩(同阳/同阴) / 劫财(阴阳不同)
    - 日主克目标 → 偏财(阴阳相同) / 正财(阴阳不同)
    - 目标克日主 → 偏官(阴阳相同) / 正官(阴阳不同)
    - 日主生目标 → 食神(阴阳相同) / 伤官(阴阳不同)
    - 目标生日主 → 偏印(阴阳相同) / 正印(阴阳不同)
    """
    day_element, day_polarity = STEM_INFO[day_stem]
    target_element, target_polarity = STEM_INFO[target_stem]

    # 判断两者阴阳是否相同(比如"甲"和"丙"都是阳,"乙"和"丁"都是阴)
    same_polarity = day_polarity == target_polarity

    if target_element == day_element:
        return "比肩" if same_polarity else "劫财"
    elif GENERATES[day_element] == target_element:
        # 日主生出的五行
        return "食神" if same_polarity else "伤官"
    elif GENERATES[target_element] == day_element:
        # 生出日主的五行
        return "偏印" if same_polarity else "正印"
    elif CONTROLS[day_element] == target_element:
        # 日主克制的五行
        return "偏财" if same_polarity else "正财"
    elif CONTROLS[target_element] == day_element:
        # 克制日主的五行
        return "偏官" if same_polarity else "正官"
    else:
        # 理论上五行生克关系是完备的,不应该走到这里
        raise ValueError(f"无法判断{day_stem}对{target_stem}的十神关系")

def build_archetype_title(day_stem: str, month_stem: str) -> str:
    """
    根据日主天干和月柱天干,生成人格原型称号。
    这是一个纯函数,用于服务端校验。
    """
    base = ARCHETYPE_BASE[day_stem]
    month_ten_god = get_ten_god(day_stem, month_stem)
    modifier = TEN_GOD_MODIFIER[month_ten_god]
    return f"{base} × {modifier}"
    
@tool
def ten_gods_tool(year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str) -> str:
    """
    根据完整的八字四柱(年柱、月柱、日柱、时柱),计算年柱、月柱、时柱各自的
    天干,相对于日主(日柱天干)的十神关系(比肩、正财、七杀等)。

    在需要分析八字中的十神关系时,必须调用此工具获取准确结果,不要凭语言模型
    自身知识猜测十神,十神的判定有严格的五行生克规则,必须依赖精确计算,
    不能靠语言模型自己推算。
    """
    # 日柱的第一个字,就是"日主"本身
    day_stem = day_pillar[0]

    # 分别取出年柱、月柱、时柱各自的天干(每个柱的第一个字)
    pillars_to_check = {
        "年柱": year_pillar[0],
        "月柱": month_pillar[0],
        "时柱": hour_pillar[0],
    }

    results = []
    for pillar_name, stem in pillars_to_check.items():
        ten_god = get_ten_god(day_stem, stem)
        results.append(f"{pillar_name}天干「{stem}」相对日主「{day_stem}」为「{ten_god}」")

    return f"日主为「{day_stem}」。" + "；".join(results)

def load_wuxing_knowledge(file_path:str)->list[Document]:
    """
    解析五行/十神知识库文件,每条记录转成一个Document。
    """
    with open(file_path,encoding="utf-8") as f:
        raw_text=f.read()

        # 按###分隔符切开每条记录,并过滤掉切分产生的空字符串
        entries=[e.strip() for e in raw_text.split("###") if e.strip()]

        documents=[]
        for entry in entries:
            lines=entry.strip().split("\n")
            metadata={}
            content_lines=[]

            for line in lines:
                if line.startswith("topic:"):
                    metadata["topic"]=line.replace("topic:","").strip()
                elif line.startswith("content:"):
                    content_lines.append(line.replace("content:","").strip())

            content='\n'.join(content_lines)
            documents.append(Document(page_content=content,metadata=metadata))
        return documents                

@tool
def archetype_naming_tool(day_stem: str, month_stem: str) -> str:
    """
    根据日主天干和月柱天干,生成这个人的"人格原型称号"(双层命名:
    日主原型 + 月柱十神修饰)。这个称号是产品的核心身份标签,
    必须调用此工具获取,不要自己编造称号文字,因为称号的命名规则是固定的,
    相同的日主和月柱组合必须始终生成相同的称号,以保证产品的一致性。
    """
    return build_archetype_title(day_stem, month_stem)

# 加载知识库（使用相对路径）
BASE_DIR = Path(__file__).parent
knowledge_path = BASE_DIR / "knowledge.txt"
wuxing_docs = load_wuxing_knowledge(str(knowledge_path))

# 在建库/加载完wuxing_docs之后,构建这个字典(只需要构建一次)
wuxing_dict = build_wuxing_dict(wuxing_docs)

# 给HuggingFace提供加速
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 向量库路径
vectorstore_path = BASE_DIR / "wuxing_chroma_db"

# 启动时若向量库目录已存在,先删除再重建
if vectorstore_path.exists():
    import shutil
    shutil.rmtree(vectorstore_path)

# 计算embedding、建向量库
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5"
)

wuxing_vectorstore = Chroma.from_documents(
    documents=wuxing_docs,
    embedding=embeddings,
    persist_directory=str(vectorstore_path)
)

wuxing_retriever=wuxing_vectorstore.as_retriever(search_kwargs={"k":2})

# ========== 第二步:初始化大模型 ==========
llm=ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.getenv("DPS_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.6,
    #关闭思考模式，才能接收tool_choice(控制模型工具调用)参数
    extra_body={"thinking":{"type":"disabled"}}
)

# ========== 第三步:组装Agent ==========
agent=create_agent(
    model=llm,

    # tools 是一个列表,把所有Agent可以调用的工具都放进去
    # 现在先只放一个排盘计算工具,验证最基础的"工具调用"链路能不能跑通
    tools=[bazi_calculator_tool,wuxing_knowledge_tool, ten_gods_tool,archetype_naming_tool],

    # system_prompt 用来定义Agent的角色、行为准则
    # 这里明确要求它"必须先调用工具算排盘,再基于结果做解读",
    # 目的是防止LLM偷懒,直接凭"感觉"编一个排盘结果出来
   system_prompt = (
    "你是一位擅长用简洁、克制、有意境的现代中文,书写人物侧写的内容创作者。"
    "你需要把传统八字命理,转化成一套现代人愿意阅读、认同、分享的人格类型内容。" \
    "内容必须紧密结合这个人具体的十神组合与五行特质,写出只属于这一种"
    "八字组合的观察,不能写成放在任何人身上都成立的通用性格描述。"
    "比如,如果十神里有'伤官',可以体现在\"擅长表达/有创造力/不喜欢被"
     "框住\"这样具体的行为细节上,而不是泛泛地说\"你很有想法\"。"
    ""
    "请严格按照以下步骤操作:"
    "第一步:调用 bazi_calculator_tool,获取准确的年柱、月柱、日柱、时柱。"
    "第二步:调用 ten_gods_tool,计算年柱、月柱、时柱天干相对日主的十神关系。"
    "第三步:调用 archetype_naming_tool,获取人格原型称号(archetype_title),"
    "这个称号必须原样使用,不能自己改写。"
    "第四步:必须依次对以下内容调用 wuxing_knowledge_tool 查询,一个都不能省略:"
    "(1) 排盘结果中出现的每一个天干地支;"
    "(2) 第二步计算出的每一个十神名称(如正官、偏财、伤官等)。"
    "即使你认为自己已经知道某个十神代表什么,也必须调用工具查询,获取"
    "知识库中准备好的具体素材,不允许仅凭自己的记忆或理解来写作十神相关内容。"
    "第五步:基于以上信息,创作最终内容,写作要求如下:"
    ""
    "语言风格:"
    "- 用现代白话文写作,句子要短、克制、留有余地,不要写成古文或诗词腔调,"
    "  不要使用'之''也''者''矣'等文言虚词,也不要模仿命理典籍的行文方式。"
    "- 绝对禁止在文案正文里出现任何命理术语或黑话,包括但不限于:"
    "  '年柱''月柱''日柱''时柱''日坐''月令''年上''生于某月''时柱再见'"
    "  '某某为某某之金/木/水/火/土'等。这些术语只能作为你写作时的内部理解,"
    "  不能出现在最终呈现给用户的文字里。"
    "- 避免网络流行语、热梗和'你以为...其实...'这类调侃、评判式的句式,"
    "  也避免'审美洁癖''死要面子'这类被用滥的网络套话。"
    "- 语气平视、懂得,像一位了解这个人的朋友在描述,不是命理先生在解签,"
    "  也不是网络博主在调侃。"
    "- 可以用一两个精准、克制的意象或比喻,但不要堆砌辞藻,一段话里"
    "  最多出现一到两个比喻,其余用直白但有分寸感的现代语言表达。"
    "- 句子偏短,段落有呼吸感,不要写成一整段绵密不断的长句。"
    "- 用现代白话文写作,句子要短、克制、留有余地,不要写成古文或诗词腔调。"
    "- 绝对禁止在文案正文里出现任何命理术语或黑话..."
    ""
    "绝不能编造排盘结果、十神关系或称号,这些必须来自工具调用的真实结果。"
    "写作要求如下:"
    ""
    "结构要求:"
    "- personality_summary不是特质罗列,而是一段有内在逻辑的短文。"
    "  建议遵循这样的行文脉络:先给出一个整体的第一印象,然后用'但''其实'"
    "  '只是'这类转折词,引出一层更深的、不那么容易被看见的特质,"
    "  让读者感受到'原来如此'的层次感,而不是罗列并列的观察。"
    "- 全文应该像一次完整的凝视,而不是拼贴几个互不相关的判断句。"
    "  句子之间要有呼应和递进,不要每句话切换一个新的、不相关的话题。"
    ""
    
),
    response_format=ToolStrategy(BaziAnalysis)#显式指定"工具调用"路径来拼装结构化结果
)

def run_analysis(year: int, month: int, day: int, hour: int) -> dict:
    """
    调用 Agent 并返回 BaziAnalysis 的 dict(model_dump)。
    """
    user_message = f"我是{year}年{month}月{day}日{hour}点出生的,帮我看看八字性格"

    result = agent.invoke({
        "messages": [("human", user_message)]
    })

    # 返回结构化响应的字典形式
    return result["structured_response"].model_dump()

# ========== 第四步:测试调用 ==========
if __name__=="__main__":
    # invoke 的输入格式是 LangChain Agent 约定的标准格式:
    # 一个包含 "messages" 的字典,messages 是一个列表,
    # 每一条消息是一个 (角色, 内容) 的元组,"human" 表示这是用户说的话
    result = agent.invoke({
        "messages": [
            ("human", "我是2006年7月21日早上7点出生的,帮我看看八字性格")
        ]
    })

    # Agent的返回结果里,messages 是完整的对话过程(包括中间工具调用的记录),
    # 我们只关心最后一条,也就是Agent最终给用户的回复
    final_message = result["messages"][-1]
    print("=== Agent 最终回复 ===")
    print(final_message.content)

    # 建议顺便把完整的中间过程也打印出来看看,
    # 这样能验证Agent是不是真的调用了工具,而不是自己瞎编的
    print("\n=== 完整对话过程(用于调试,查看Agent是否真的调用了工具) ===")
    for msg in result["messages"]:
        print(f"[{type(msg).__name__}] {msg.content if hasattr(msg, 'content') else msg}")