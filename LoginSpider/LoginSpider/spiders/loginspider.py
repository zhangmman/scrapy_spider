import scrapy
from scrapy.http import Request, FormRequest
from LoginSpider.items import LoginspiderItem


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["example.webscraping.com"]
    start_urls = ['http://example.webscraping.com/places/default/user/login?_next=/places/default/index']

    def parse(self, response):
        # 登入成功后，需要进入profile界面（点击下拉菜单另个一界面）
        profile = response.xpath('//*[@id="navbar"]/li/ul/li[1]/a/@href').getall()[0]
        profile_url = 'http://example.webscraping.com' + profile
        yield Request(profile_url)

        # 解析登录后下载的页面， 此例中为用户个人信息页面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        g1 = [x for x in range(1, len(keys))]
        for i in g1:
            result = LoginspiderItem()
            print(keys[i])
            result['key'] = keys[i]
            result['value'] = values[i]
            yield result

    # 登录页面的url
    # login_url = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'
    # 覆写基类的start_requests方法， 最先请求登录页面。
    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.login)

    def login(self, response):
        # 登录页面的解析函数， 构造FormRequest对象提交表单
        print('# 登录页面的解析函数， 构造FormRequest对象提交表单')
        fd = {'email': 'zhangman@ncepu.cn', 'password': '*********'}
        print('尝试登入！！！！！！！！')
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)
        print('********你好啊 **********')

    def parse_login(self, response):
        # 登录成功后， 继续爬取start_urls 中的页面
        print('验证是否登入成功')
        if 'Welcome man' in response.text:
            print('登入成功了！！！！！！！！')
            yield from super().start_requests()   # 调用基类的start_requests方法

