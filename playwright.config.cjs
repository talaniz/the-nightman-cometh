const {defineConfig}=require('@playwright/test');
const port=process.env.NIGHTMAN_PORT||'8773';
module.exports=defineConfig({
 outputDir:process.env.NIGHTMAN_RESULTS||'test-results',testDir:'tests/browser',testMatch:'*.spec.cjs',timeout:240000,workers:1,fullyParallel:false,
 use:{viewport:{width:1280,height:720},trace:'retain-on-failure',baseURL:`http://127.0.0.1:${port}`},
 projects:[{name:'chromium',use:{browserName:'chromium',launchOptions:{executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox','--disable-gpu']}}},{name:'firefox',use:{browserName:'firefox'}}],
 webServer:{command:`python3 tools/serve_preview.py --root ${process.env.NIGHTMAN_BUILD||'build/web'} --port ${port}`,url:`http://127.0.0.1:${port}`,reuseExistingServer:false,timeout:10000}
});
