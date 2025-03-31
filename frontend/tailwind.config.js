/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts}",
    "./node_modules/flowbite/**/*.js",
    "./node_modules/flowbite-vue/**/*.js",
  ],
  theme: {
    extend: {},
    colors: {
      BbWhite: "#FFFFFF",
      BbLightBrown: "#CAB7A1",
      BbLightPurple: "#F6EDFA",
      BbRed: "#D82B1E",
      BbDarkBlue: "#292F36",
      BbSkyDark: "#064C72",
      BbSkyeMedium: "#026C80",
      BbSkyeLight: "#8DB4AD",
      BbBeige: "#ECAE7D",
      BbBurntOrange: "#ED6335",
      BbPink: "#E53373"
  },
  },
  plugins: [
    require("flowbite/plugin"),
    require('tailwind-scrollbar-hide')
  ],
}
