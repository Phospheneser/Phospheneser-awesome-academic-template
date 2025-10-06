// 占卜小人功能实现
class Diviner {
  constructor() {
    this.container = null;
    this.divineWindow = null;
    this.divineMode = 'JiuGongLiuRen'; // 默认占卜模式
    this.query = '今日运势'; // 默认查询
    this.isDragging = false;
    this.offsetX = 0;
    this.offsetY = 0;
  }

  // 初始化占卜小人
  init() {
    // 创建占卜小人容器
    this.container = document.createElement('div');
    this.container.id = 'diviner-container';
    this.container.className = 'diviner-container';
    this.container.style.position = 'fixed';
    this.container.style.bottom = '80px';
    this.container.style.right = '20px';
    this.container.style.zIndex = '1001';
    this.container.style.cursor = 'pointer';
    this.container.style.transition = 'transform 0.3s ease';

    // 添加占卜小人图标
    const divinerIcon = document.createElement('img');
    divinerIcon.src = './media/divine/fortuneteller.svg';
    divinerIcon.alt = 'Fortuneteller';
    divinerIcon.style.width = '60px';
    divinerIcon.style.height = '60px';
    this.container.appendChild(divinerIcon);

    // 添加悬停效果
    this.container.addEventListener('mouseover', () => {
      this.container.style.transform = 'scale(1.1)';
    });
    this.container.addEventListener('mouseout', () => {
      this.container.style.transform = 'scale(1)';
    });

    // 添加点击事件，打开占卜窗口
    this.container.addEventListener('click', () => {
      this.openDivineWindow();
    });

    // 添加拖拽功能
    this.container.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      const rect = this.container.getBoundingClientRect();
      this.offsetX = e.clientX - rect.left;
      this.offsetY = e.clientY - rect.top;
    });

    document.addEventListener('mousemove', (e) => {
      if (this.isDragging) {
        e.preventDefault();
        const x = e.clientX - this.offsetX;
        const y = e.clientY - this.offsetY;
        
        // 确保不超出窗口边界
        const maxX = window.innerWidth - this.container.offsetWidth;
        const maxY = window.innerHeight - this.container.offsetHeight;
        
        this.container.style.left = Math.max(0, Math.min(x, maxX)) + 'px';
        this.container.style.top = Math.max(0, Math.min(y, maxY)) + 'px';
        this.container.style.bottom = 'auto';
        this.container.style.right = 'auto';
      }
    });

    document.addEventListener('mouseup', () => {
      this.isDragging = false;
    });

    // 添加到页面
    document.body.appendChild(this.container);
  }

  // 打开占卜窗口
  openDivineWindow() {
    if (this.divineWindow) {
      return;
    }

    // 创建占卜窗口
    this.divineWindow = document.createElement('div');
    this.divineWindow.id = 'divine-window';
    this.divineWindow.className = 'divine-window';
    this.divineWindow.style.position = 'fixed';
    this.divineWindow.style.bottom = '80px';
    this.divineWindow.style.right = '20px';
    this.divineWindow.style.width = '350px';
    this.divineWindow.style.maxHeight = '600px';
    this.divineWindow.style.backgroundColor = 'white';
    this.divineWindow.style.borderRadius = '10px';
    this.divineWindow.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.2)';
    this.divineWindow.style.padding = '20px';
    this.divineWindow.style.zIndex = '1002';
    this.divineWindow.style.overflow = 'auto';
    
    // 添加关闭按钮
    const closeBtn = document.createElement('button');
    closeBtn.innerText = '×';
    closeBtn.style.position = 'absolute';
    closeBtn.style.top = '10px';
    closeBtn.style.right = '10px';
    closeBtn.style.width = '30px';
    closeBtn.style.height = '30px';
    closeBtn.style.border = 'none';
    closeBtn.style.backgroundColor = 'transparent';
    closeBtn.style.fontSize = '24px';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.color = '#666';
    closeBtn.addEventListener('click', () => {
      this.closeDivineWindow();
    });
    this.divineWindow.appendChild(closeBtn);

    // 添加标题
    const title = document.createElement('h3');
    title.innerText = '神秘占卜师';
    title.style.textAlign = 'center';
    title.style.color = '#8B0000';
    title.style.marginBottom = '20px';
    title.style.fontFamily = 'Pacifico, cursive';
    title.style.fontSize = '24px';
    this.divineWindow.appendChild(title);

    // 添加查询输入
    const queryLabel = document.createElement('label');
    queryLabel.innerText = '请输入您的问题：';
    queryLabel.style.display = 'block';
    queryLabel.style.marginBottom = '10px';
    queryLabel.style.color = '#333';
    this.divineWindow.appendChild(queryLabel);

    const queryInput = document.createElement('input');
    queryInput.type = 'text';
    queryInput.id = 'divine-query';
    queryInput.value = this.query;
    queryInput.style.width = '100%';
    queryInput.style.padding = '8px';
    queryInput.style.marginBottom = '15px';
    queryInput.style.border = '1px solid #ddd';
    queryInput.style.borderRadius = '5px';
    queryInput.addEventListener('input', () => {
      this.query = queryInput.value;
    });
    this.divineWindow.appendChild(queryInput);

    // 添加占卜模式选择
    const modeLabel = document.createElement('label');
    modeLabel.innerText = '选择占卜方式：';
    modeLabel.style.display = 'block';
    modeLabel.style.marginBottom = '10px';
    modeLabel.style.color = '#333';
    this.divineWindow.appendChild(modeLabel);

    const modeContainer = document.createElement('div');
    modeContainer.style.marginBottom = '15px';
    
    const modes = [
      { id: 'JiuGongLiuRen', name: '九宫六壬' },
      { id: 'LiuYaoQiGua', name: '六爻起卦' },
      { id: 'Tarot', name: '塔罗牌' }
    ];

    modes.forEach(mode => {
      const modeOption = document.createElement('div');
      modeOption.style.marginBottom = '5px';
      
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.id = `mode-${mode.id}`;
      radio.name = 'divine-mode';
      radio.value = mode.id;
      radio.checked = mode.id === this.divineMode;
      radio.addEventListener('change', () => {
        this.divineMode = mode.id;
      });
      
      const modeLabel = document.createElement('label');
      modeLabel.htmlFor = `mode-${mode.id}`;
      modeLabel.innerText = mode.name;
      modeLabel.style.marginLeft = '5px';
      modeLabel.style.cursor = 'pointer';
      
      modeOption.appendChild(radio);
      modeOption.appendChild(modeLabel);
      modeContainer.appendChild(modeOption);
    });

    this.divineWindow.appendChild(modeContainer);

    // 添加占卜按钮
    const divineBtn = document.createElement('button');
    divineBtn.innerText = '开始占卜';
    divineBtn.style.width = '100%';
    divineBtn.style.padding = '10px';
    divineBtn.style.backgroundColor = '#8B0000';
    divineBtn.style.color = 'white';
    divineBtn.style.border = 'none';
    divineBtn.style.borderRadius = '5px';
    divineBtn.style.cursor = 'pointer';
    divineBtn.style.fontSize = '16px';
    divineBtn.addEventListener('click', () => {
      this.startDivination();
    });
    this.divineWindow.appendChild(divineBtn);

    // 添加结果区域
    const resultContainer = document.createElement('div');
    resultContainer.id = 'divine-result';
    resultContainer.style.marginTop = '20px';
    resultContainer.style.padding = '15px';
    resultContainer.style.backgroundColor = '#f9f9f9';
    resultContainer.style.borderRadius = '5px';
    resultContainer.style.minHeight = '100px';
    resultContainer.style.whiteSpace = 'pre-wrap';
    resultContainer.style.fontFamily = 'Noto Sans, sans-serif';
    this.divineWindow.appendChild(resultContainer);

    // 添加到页面
    document.body.appendChild(this.divineWindow);
  }

  // 关闭占卜窗口
  closeDivineWindow() {
    if (this.divineWindow) {
      document.body.removeChild(this.divineWindow);
      this.divineWindow = null;
    }
  }

  // 开始占卜
  async startDivination() {
    const resultContainer = document.getElementById('divine-result');
    resultContainer.innerText = '占卜中...';
    
    try {
      // 调用Python服务器获取真实的占卜结果
      const result = await this.getDivineResultFromServer();
      resultContainer.innerText = result;
    } catch (error) {
      // 如果API调用失败，使用模拟结果作为备选
      console.warn('API调用失败，使用模拟结果：', error);
      try {
        const mockResult = this.mockDivineResult();
        resultContainer.innerText = `(使用模拟结果)\n${mockResult}`;
      } catch (mockError) {
        resultContainer.innerText = `占卜失败：${error.message}\n\n请确保Python服务器已启动。\n启动方法：cd static/python/diviner && python3 divine_server.py`;
      }
    }
  }

  // 从服务器获取占卜结果 - 重写版本以解决URL问题
  async getDivineResultFromServer() {
    // 获取服务器地址的优先级：
    // 1. URL参数 (用于临时测试)
    // 2. localStorage (用于持久化设置)
    // 3. meta配置 (默认值)
    let serverUrl = 'http://localhost:8000'; // 默认值
    
    // 检查URL参数
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('serverUrl')) {
      serverUrl = urlParams.get('serverUrl');
      console.log('从URL参数获取服务器地址:', serverUrl);
    }
    // 检查localStorage
    else if (localStorage.getItem('divineServerUrl')) {
      serverUrl = localStorage.getItem('divineServerUrl');
      console.log('从localStorage获取服务器地址:', serverUrl);
    }
    // 最后检查meta配置
    else if (window.metaConfig?.divine?.serverUrl) {
      serverUrl = window.metaConfig.divine.serverUrl;
      console.log('从meta配置获取服务器地址:', serverUrl);
    }
    
    // 确保serverUrl格式正确，没有尾部斜杠
    serverUrl = serverUrl.replace(/\/$/, '');
    
    // 构造正确的API请求URL，使用/divine路径
    const divinePath = 'divine';
    const queryParams = new URLSearchParams();
    queryParams.append('type', this.divineMode);
    queryParams.append('query', this.query);
    const apiUrl = `${serverUrl}/${divinePath}?${queryParams.toString()}`;
    
    // 添加详细的调试日志，确认构造的URL
    console.log('构造的API请求URL:', apiUrl);
    
    // 设置超时处理
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10秒超时
    
    try {
      // 发送GET请求到Python服务器
      console.log('准备发送请求到:', apiUrl);
      const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        signal: controller.signal
      });
      
      // 清除超时计时器
      clearTimeout(timeoutId);
      
      // 记录响应状态
      console.log('服务器响应状态:', response.status);
      
      // 检查响应状态
      if (!response.ok) {
        throw new Error(`服务器响应错误：${response.status}`);
      }
      
      // 解析JSON响应
      const data = await response.json();
      
      // 检查占卜是否成功
      if (!data.success) {
        throw new Error(data.error || '占卜过程中发生错误');
      }
      
      // 返回占卜结果
      return data.result;
    } catch (error) {
      // 统一错误处理
      console.error('API调用错误:', error);
      if (error.name === 'AbortError') {
        throw new Error('服务器响应超时，请检查服务器是否正常运行');
      } else if (error.message.includes('Failed to fetch')) {
        throw new Error('无法连接到占卜服务器，请确保服务器已启动\n提示：请尝试清除浏览器缓存（Ctrl+F5）后重试');
      }
      throw error;
    }
  }

  // 模拟占卜结果（作为备选）
  mockDivineResult() {
    const baseResult = `对于您的问题：【${this.query}】\n\n`;
    
    switch (this.divineMode) {
      case 'JiuGongLiuRen':
        const jiuGongResults = [
          '【大安（震）（木）：平安吉祥，诸事顺遂】->【速喜（离）（火）：喜事临门，好消息快来】->【小吉（巽）（木）：小有收获，平稳略好】',
          '【留连（坎）（水）：事情拖延，难以决断】->【小吉（巽）（木）：小有收获，平稳略好】->【大安（震）（木）：平安吉祥，诸事顺遂】',
          '【速喜（离）（火）：喜事临门，好消息快来】->【大安（震）（木）：平安吉祥，诸事顺遂】->【桃花（艮）（土）：姻缘桃花，人际和谐】',
          '【赤口（兑）（金）：口舌是非，易生争执】->【留连（坎）（水）：事情拖延，难以决断】->【天德（乾）（金）：吉祥如意，贵人相助】',
          '【小吉（巽）（木）：小有收获，平稳略好】->【天德（乾）（金）：吉祥如意，贵人相助】->【速喜（离）（火）：喜事临门，好消息快来】'
        ];
        return baseResult + jiuGongResults[Math.floor(Math.random() * jiuGongResults.length)];
        
      case 'LiuYaoQiGua':
        const liuYaoResults = [
          '得到的是【乾卦(刚健中正)】\n卦辞为：【元亨利贞】\n解释为：大吉大利，亨通顺利，坚守正道。\n性质是：【大吉】',
          '得到的是【坤卦(柔顺厚德)】\n卦辞为：【元亨利牝马之贞】\n解释为：大吉大利，像母马一样坚守正道。\n性质是：【吉】',
          '得到的是【屯卦(始生难)】\n初爻爻变，爻辞为：【磐桓，利居贞，利建侯】\n解释为：徘徊不前，利于守正，利于建立诸侯。\n吉凶：【吉】',
          '得到的是【蒙卦(启蒙)】\n二爻爻变，爻辞为：【包蒙，吉。纳妇，吉。子克家】\n解释为：包容蒙昧，吉祥。迎娶妻子，吉祥。儿子能够治家。\n吉凶：【吉】',
          '得到的是【需卦(等待)】\n上爻爻变，爻辞为：【入于穴，有不速之客三人来，敬之终吉】\n解释为：进入洞穴，有不请自来的三位客人，恭敬对待他们最终吉祥。\n吉凶：【吉】'
        ];
        return baseResult + liuYaoResults[Math.floor(Math.random() * liuYaoResults.length)];
        
      case 'Tarot':
        const tarotResults = [
          '过去 :【正位 魔术师 : 创造与自信】\n现在 :【正位 恋人 : 选择与和谐】\n未来 :【正位 太阳 : 成功与快乐】',
          '过去 :【逆位 月亮 : 困惑与恐惧】\n现在 :【正位 星星 : 希望与信念】\n未来 :【正位 审判 : 重生与觉醒】',
          '过去 :【正位 女祭司 : 智慧与直觉】\n现在 :【正位 皇帝 : 权威与控制】\n未来 :【逆位 战车 : 冲突与挫折】',
          '过去 :【正位 愚人 : 冒险与新开始】\n现在 :【逆位 隐士 : 孤独与内省】\n未来 :【正位 世界 : 完成与圆满】',
          '过去 :【逆位 命运之轮 : 停滞与挑战】\n现在 :【正位 力量 : 勇气与耐心】\n未来 :【正位 节制 : 平衡与和谐】'
        ];
        return baseResult + tarotResults[Math.floor(Math.random() * tarotResults.length)];
        
      default:
        return baseResult + '未知的占卜方式';
    }
  }
}

// 初始化占卜小人
function initDiviner() {
  try {
    // 检查是否存在全局metaConfig对象并且明确禁用了占卜小人
    if (typeof window !== 'undefined' && window.metaConfig && window.metaConfig.add_diviner === false) {
      return;
    }
    
    // 检查是否存在全局meta_config对象并且明确禁用了占卜小人
    if (typeof window !== 'undefined' && window.meta_config && window.meta_config.add_diviner === false) {
      return;
    }
    
    // 检查是否存在局部metaConfig变量并且明确禁用了占卜小人
    if (typeof metaConfig !== 'undefined' && metaConfig && metaConfig.add_diviner === false) {
      return;
    }
    
    // 默认情况下初始化占卜小人（除非明确禁用）
    const diviner = new Diviner();
    diviner.init();
  } catch (error) {
    console.warn('初始化占卜小人时发生错误:', error);
    // 即使出错，也尝试初始化占卜小人
    try {
      const diviner = new Diviner();
      diviner.init();
    } catch (innerError) {
      console.error('无法初始化占卜小人:', innerError);
    }
  }
}

/**
 * 全局帮助函数：设置或清除服务器地址
 * 使用方法：
 * - 设置服务器地址: setDivineServerUrl('https://your-server-url.com')
 * - 清除服务器地址设置: setDivineServerUrl(null)
 * @param {string|null} url - 服务器地址，为null时清除设置
 */
window.setDivineServerUrl = function(url) {
  if (url) {
    // 确保URL格式正确，添加http或https协议
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      console.warn('警告：URL应包含协议(http://或https://)，已自动添加https://');
      url = 'https://' + url;
    }
    
    // 去除尾部斜杠
    url = url.replace(/\/$/, '');
    
    localStorage.setItem('divineServerUrl', url);
    console.log('服务器地址已保存到localStorage:', url);
    console.log('请刷新页面以应用新的服务器地址设置。');
  } else {
    localStorage.removeItem('divineServerUrl');
    console.log('已清除localStorage中的服务器地址设置，将使用默认配置。');
    console.log('请刷新页面以应用默认设置。');
  }
};