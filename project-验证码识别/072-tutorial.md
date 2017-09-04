## 前言
	没有学校图书馆帐号的人被鄙视呀，尤其是什么哈士奇。偶然发现，某东居然有个验证码供我玩玩，而且这个验证码不是太难。
	隧，决定搞它一搞

#### 1. 搭建环境
```python
# 自己动手吧，自已动手丰衣足食
from selenium import webdriver
import time
import os
import pytesseract
from PIL import ImageEnhance, Image

# 根据引入包，自己安装吧，
```

#### 2. 启动浏览器驱动
```python
dist_url = 'https://www.jd.com/'
driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
driver.get(dist_url)

# 此处我有话讲，
# 小弟一直在用chrome浏览器，没有遵循哈士奇的要求使用Firfox，请多见识
# 使用chrome最主要的是要配置chromedriver，这个也是百度一大堆
```

#### 3. 对页面上验证码部分进行截图
```python
def crop_image_code(box=(510,512,569,537)):
    driver.get_screenshot_as_file('./screen.jpg')
    im = Image.open('./screen.jpg')
    # box = (510,512,569,537)   # 设置要裁剪的区域
    region = im.crop(box)
    region.save('./image_code.png')
    return 'image_code.png'

 # 此处是主要的注意点是要手动测量截图区域，
 # 这个现在也好办的很，找个截图工具随便一测量就ok

```

#### 4. win上识别图片需要用到`Tesseract-OCR`
```python
# Tesseract-OCR请百度自行安装，不要问我为什么要用它，我也不知道的

def image_file_to_string(file):
    time.sleep(1)
    cwd = os.getcwd()
    try:
        os.chdir('C:\\Tesseract-OCR')
        imgfile = Image.open(file)
        return pytesseract.image_to_string(imgfile)
    finally:
        os.chdir(cwd)
```
#### 5. 识别验证码最主要的部分，暴力识别，不识别出势不罢休，非要刷死你
```python
# 这里自己要找一个终止条件，否则识别正确了，再刷新验证码你就完蛋了
# 其实最简单的也就是当前页面元素找不到的时候也就是页面已经跳转了，也即是成功了
while True:
    time.sleep(1)
    try:
        elem_submit = driver.find_element_by_id('order-submit')
        elem_code = driver.find_element_by_id('checkcodeTxt')

        # 如果验证码已经有了，则跳过，等待页面跳转
        if getattr(elem_code, 'text'):
            continue
        # 终于到验证码的问题了
        img_code_path = crop_image_code(box=(740,101, 926,146))
        img_code_2 = sharpness_image_code('./' + img_code_path)
        code = image_file_to_string('D:\\python-learning\learning-group\library-auto\\' + img_code_2)
        if code:
            # 填入验证码，并提交
            elem_code.send_keys(code)
            elem_submit.click()
        else:
            # 刷新验证码
            driver.find_element_by_id('orderCheckCodeImg').click()
    except Exception:
        if driver.window_handles[1]:
            driver.switch_to.window(driver.window_handles[1])
            driver.get_screenshot_as_file('./success.jpg')
            break;
```

#### 6. 最后需要说明的一点
```python
# 将页面滚动底部，识图验证码和提交
time.sleep(2)
js = 'window.scrollTo(0,document.body.scrollHeight)'
driver.execute_script(js)
```

## 我最后要说的话
	1. 我为了满足客代表尽快收到pr的愿望，教程写的不是很仔细
	2. 不知道是不是我刷京东验证的原因，现在京东提交订单时的验证码不在了




