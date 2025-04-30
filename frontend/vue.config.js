const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  outputDir: '../backend/app/static',
  assetsDir: 'static',
  publicPath: '/static/',
  indexPath: '../templates/index.html',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      }
    }
  }
})
