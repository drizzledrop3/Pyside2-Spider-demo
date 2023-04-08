# Pyside2-demo
基于爬虫与Pyside2库实现一个小说下载器



爬取的三个网站如下：

1. ```
   url = "https://www.aixdzs.com/"
   ```

2. ```
   url = "https://www.xbiquge.la/"
   ```

3. ```
   url = "http://www.bige3.com/"
   ```

它们如果G了那自然功能也是G了的，但是思路很简单了，用到别的小说网站也是一样的。

以上三个下载路径都因为没啥反爬机制，爬取较易，但是还是由于频繁爬取会封IP，未实现异步，如果想优化下载速度，可以考虑`异步+IP池`。

其实还给了第四个下载路径，用`Selenium实现`的，但是考虑到可移植性，在放到GitHub时就舍弃了，但该说不说，在不会js逆向的时候，Selenium真好用啊(笑)




```python
"""
  Python Spider + QT demo
  @author:drizzledrop
  @time:2022.07.29
"""
```

