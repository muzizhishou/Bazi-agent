/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'calligraphy': ['Ma Shan Zheng', 'ZCOOL XiaoWei', 'cursive'],
        'serif': ['Noto Serif SC', 'LXGW WenKai', 'STSong', 'SimSun', 'serif'],
        'sans': ['PingFang SC', '-apple-system', 'system-ui', 'sans-serif'],
      },
      colors: {
        // 中国传统色
        vermilion: '#E63946', // 朱砂红（印章专用）
        xuan: {
          paper: '#F9F6F0', // 宣纸底
          warm: '#F5F1E8',
          moon: '#E8E4D9',
        },
        ink: {
          deep: '#2B2B2B', // 墨底
          black: '#1C1C1C',
          gray: '#4A4A4A',
        },
        element: {
          metal: {
            moon: '#E8E4D9', // 月白
            silver: '#C0C0C0', // 银灰
            bronze: '#8C6239', // 古铜
          },
          wood: {
            indigo: '#2E4E7E', // 青黛
            bamboo: '#5A7C65', // 竹青
            stone: '#4A7C59', // 石绿
          },
          water: {
            indigo: '#2C4F7C', // 靛青
            navy: '#1C3D5A', // 黛蓝
          },
          fire: {
            rouge: '#B85C5C', // 胭脂
            ochre: '#A0522D', // 赭红
          },
          earth: {
            ochre: '#9D7D54', // 赭石
            camel: '#A67C52', // 驼色
          }
        }
      }
    },
  },
  plugins: [],
}
