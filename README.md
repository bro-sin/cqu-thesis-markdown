# 模版说明

- [模版说明](#模版说明)
  - [运行](#运行)
  - [样式](#样式)
  - [命令定义](#命令定义)
  - [交叉引用参数设定](#交叉引用参数设定)
  - [开发日志](#开发日志)
  - [第一阶段](#第一阶段)
    - [项目TODO](#项目todo)
    - [模版TODO](#模版todo)
    - [代码TODO](#代码todo)
  - [第二阶段](#第二阶段)
    - [项目TODO](#项目todo-1)
    - [模版 TODO](#模版-todo)
    - [文档TODO](#文档todo)
  - [无法实现](#无法实现)
    - [可以通过后处理脚本实现](#可以通过后处理脚本实现)

## 运行

```text
pandoc example.md  --filter equations_no.py --filter header_convert.py --filter figures_no.py --filter refs.py --filter texcommands.py -o example.docx --reference-doc template/reference.docx
```

## 样式

除了 pandoc 预设的那几个样式外，还有以下几种特殊样式

- `TOC Heading`: 目录标题
- `Appendix Text`: 附录正文样式
- `Heading Numbering`：标题的编号列表
- `Key Word`：“关键字”的前缀字符样式
- `Equation`：显示公式的样式，带有段前段后各一行，用来保证公式可以完整显示
- `Appendix Heading 2`: 附录二级标题
- `Appendix Heading 3`: 附录三级标题

TODO

<!-- - `Unnumbered Heading 1`: 无编号的一级标题
- `Unnumbered Heading 2`: 无编号的二级标题 -->

## 命令定义

- `标题{-}`：后面的`{-}`表示去掉某标题的编号，根据排版要求和实现方案，仅提供一级标题（适用于摘要，附录，参考文献）和二级标题（适用于附录内部的二级标题`A`,`B`等）
- `附录{- .appendix}`：`{}`中的`-`表示去掉编号，`.appendix`表示该部分是目录。因为排版要求规定附录中的字号比正文小，所以需要单独标注出附录来为附录中的正文套用单独的附录样式（见`样式`章节）
  - 实现原理：单独定义了未编号的一级标题和二级标题样式（见`样式`部分）
- `\Space{n}`：生成n个空格，用来生成`摘    要`中间的4个空格，n可为空
- `\KeyWord{关键词：}`：产生名为“关键词：”的关键词前缀，可自定义
  - 实现原理：对`{}`内的内容套用预设的`Key Word`文本样式
- `\toc{目录}`：产生标题为`目录`的目录
- `\newSection{Content}`和`\newSection{TOC}`：产生分节符，对应摘要后方的分节符和目录后方的分节符
  - 实现原理：通过文本匹配替换，直接插入对应的ooxml代码
  - 分节符的作用：控制**分节符位置前方**的页面的“页面参数”，例如纸张大小，分栏，**仅在不同的“节”中才能生成不同样式的页眉页脚**，所以为了实现不同的页眉页脚效果，必须插入分节符
- `\newLine{}`：插入换行符，在不分段的情况下进入下一行（即Word中`Shift` + `Enter`的效果），可用来产生双语题注
  - 实现原理：替换为ooxml代码或pandoc原生的`LineBreak`对象
- `\newPara{n}`：生成n个空段落，用来产生一定的间距，参数可为空
  - 要求只能在空段落中使用，即`RawBlock`，若和其他内容在同一段落，则会被解析成`RawInline`，造成错误
- `\newPage{}`：插入分页符，跳转到下一页
- `\Caption2{fig}`：插入双语题注的第二题注时，用该命令产生第二语言的编号前缀，例如中英题注中，默认会生成中文的题注编号`图1.3`，而英文题注的编号则须用该命令产生`Fig 1.3`
  - 实现原理：预设第二题注的前缀，插入域代码生成编号
- `\Reference{}`：在当前位置插入参考文献，因为排版要求规定`附录`在`参考文献`之后，而pandoc默认参考文献插入在文档最后，所以需要定义命令以在任意位置插入参考文献
- `\Style{name}`：对当前段落应用`name`样式（特殊的内置样式名称可能不一样）
  - 通过插入ooxml代码实现
- `[被标记文本]{#书签名字}`：可以对`被标记文本`标记一个名为`书签名字`的书签，通过书签和域代码配合，可以实现交叉引用。该功能为pandoc自带功能
- `## 123{#xxx}`：可对标题进行标记书签，通过`[@sec-xxx-no]`可以引用标题的编号
- `` `{some code}`{=field}``：`some code`为域代码，`{=field}`表示把该部分内容作为域代码处理，通过该语法可以实现插入自定义域代码的功能

TODO:

- 分隔线的缩进问题

## 交叉引用参数设定

- 前缀
  - 通过`xxx:`表示前缀
- 后缀
  - 通过，`-page`表示后缀
- 标记
  - 只对编号内容进行标记，题注内容的前后缀通过配置文件生成
- 书签
  - 生成的书签包括前缀而不含后缀`sec:xxx`
- 子图
- 定理
- Markdown语法
  - `sec:xxx`:生成章节号
  - `sec:xxx-c`:生成标题内容
  - `sec:xxx-page`生成页面
  - `eq:xxx`
  - `[-@eq:xxx]`只有编号
  - `fig:xxx`:图片编号
  - `fig:xxx-c`
  - `fig:xxx`
  - `thm:abc`: 定理1.2.3（abc定理）：XXX
  - `thm:abc-c`
- 实现
  - 编号前缀：
  - 编号分隔符
  - 标题深度
- 书签
  - 当没有前缀的时候，直接生成内容，`-no`生成编号

## 开发日志

- 2020.12.05~2020.12.06：
  - 总结CQU排版要求[@ilcpm]
  - python编程实现[@Hagb]
- 2020.12.07：
  - 开始模版制作
  - 遇到pandoc的bug
    - 触发条件为两端对齐+换行符，会导致第一行变成“分散对齐”的效果
    - 解决方案为：在settings.xml中添加节点

      ```xml
      <w:compat>
        <w:doNotExpandShiftReturn/>
      </w:compat>
      ```

- 2020.12.08~2020.12.09：
  - 大量完善模版和相关功能
- 2020.12.25：
  - 增加对标题编号的引用功能
  - 修改取消标题编号的逻辑，改为直接使用ooxml代码，不使用第三方样式
  - 从以前的文档中翻出一篇适作为英文模版格式参考的PDF
- 2021.01.10：
  - 根据同学的反馈增加了格式要求的细节
  - 细化排版要求
- 2021.01.19
  - [X] 再三确认带合并单元格的表格无法实现
    - 无法用公式中的表格转换
    - 也不支持文本类型的表格合并
    - 如果强行转换会非常麻烦，目前不考虑表格合并的问题
- 2021.01.24~2021.01.25
  - CQU排版要求
    - 对参考文献（重点）内容作出了重大修订
      - 查阅并验证了csl文件关于“等”的相关内容
    - 对行内公式的行高问题（重点）进行了研究并给出方案（行距设置采用“最小值”而非“固定值”）
    - 对图片&表格进行了补充
    - 补充了研究生的附录部分
    - 细节修改
  - [X] 公式行距问题
    - 正文中出现了比较高的公式，例如`\sum`，会使得20磅的行高不够，如何处理？
    - 解决方案找到，设置行距为最小值
    - [X] 修改模版
    - **删除了Unnumbered Heading样式**
  - [X] 页眉
    - [X] 页眉的标题需要编号
    - [X] 目录区域的页眉需要再单独设置右上角的样式
    - pandoc采用模版中的**第一个分节符**作为文档最后的分节符！而不是模版的最后一个分节符
  - [X] 尝试修改引用块的样式为Markdown中的样式
    - 效果不好，放弃
    - 修改引用块的边框上边距为6磅
- 2021.01.28~2021.01.29
  - 段前段后：经测试无法通过在标题段落前增加换行符来达到一模一样的手动空行的效果，因为一级标题里的换行符会被添加到页眉中
  - 行间公式间距问题
    - 发现：在正常的Word文档中，表格中的公式行距比较正常，但是在pandoc输出的文档中，公式底部看着像被裁掉了一磅左右
    - 解决：满山遍野找bug，结果发现是因为文档网格，Word默认定义了文档网格，公式被对齐到文档网格上，间距看着正常
  - pandoc发现bug
    - [ ] 网格线显示问题：在研究公式行距问题过程中，发现pandoc输出的文档无法显示“网格线”，经查是`settings.xml`文件中部分内容与常规文档有所区别，具体xml内容后期整理并提交issue
    - [ ] 含有公式的表格公式对齐问题：设置表格内容居中，公式居中，结果公式位置偏右，经查是`settings.xml`中部分设置与pandoc表格所用的ooxml代码有关，后续提issue等pandoc解决
  - 日志
    - 拆分了`文档TODO`部分，文档部分要开始写了
- 2021.02.14
  - 为公式增加了`noindent`样式
- 2021.02.15~2021.02.16
  - 增加《排版指导》
    - 完成“公式字体”部分编写
  - 完成代码文件的拆分
  - 调整排版要求文件夹结构
  - 验证脚注和内联代码的字号问题
- 2021.02.20
  - 增加用来解压和压缩docx的py文件，可能会用来修改最后生成的docx文件
    - 经验证，因为各个文件都不是直接嵌入，所以只能通过解析xml树实现对功能的实现
- 2021.02.28~2021.03.01
  - 开始制作封面
  - 对无题注的图片套用`Figure`样式
- 2021.03.06
  - 修改`Key Word`样式的使用逻辑，使用`\KeyWord{关键词}关键词1，关键词2`这样的语法
    - [X] `KeyWord{}`等语法的括号中的内容，不能用pf.str()函数来解析，会生成纯文本，应当使用原生的pandoc功能对文本进行重新解析
    - 考虑采用`\KeyWord{}xxx`这样的形式生成内容（2021.01.25）
    - 经研究发现，这样做会导致单独的`RawBlock`变成`RawInline`，就无法插入段落在其中了
    - 能否直接利用子元素获取到父元素然后在前面插入段落？
  - [X] 实现了对段落的自定义样式
- 2021.03.16
  - 优化todo，细分项目进度
  - 测试用`\newcommand{}`定义命令来替换成`ooxml`命令，失败，输出结果只能是tex命令，不支持其他格式
- 2021.03.26 
  - 开始拆分CQU模版部分
- 2021.04.02
  - 深入讨论如何插件设计，如何拆解
  - 具体到插件拆解进度，进展并不多
- 2021.04.04
  - 完成了对域代码引用功能的制作
  - [X] 域代码实现`` `qwe`{=field}``
  - [X] 引用嵌套怎么办`[@page-[@xxx]]`
- 2021.04.05
  - 完成了对嵌套解析的支持
    - [X] ★对LaTeX语法花括号中内容的嵌套解析
  - 抽离了CQU的页眉页脚配置
  - [X] 经测试，目录的标题在Windows端存在问题，待修改
    - 修改内置的目录命令为`\tocRaw`，留下`\toc`供模版定义
- 2021.04.08
  - [X] 参考文献没有超链接，无法跳转
    - 翻出了以前的工作编译脚本，找到了插入超链接的参数，解决问题
  - 文档撰写
- 2021.04.23
  - [X] 行间公式如果是出现在一个段落的中间，也就是没有分段的情况下，需要对行间公式后面的内容取消首行缩进，因为这个公式是出现在这个段落中间的
  - 测试使用`Link`域代码插入其他文档来实现表格问题，同一个文档只会出现在同一个页面，多余部分会被截去，相当于是图片，因此无法对大型表格生效，失败
  - **测试使用`IncludeText`样式嵌套外部文件实现复杂表格应用，成功！！！**
    - 空段落还存在一些问题，问题不大
  - **反馈了pandoc的换行符bug**
  - [X] ★文本的自定义样式（该如何设计语法？）
    - 采用`[text]{style="text_style_name"}`的方式
  - [X] 下划线`pf.Underline()`
    - `[text]{.underline}`或`[text]{.U}`
  - **经查，pandoc输出的文档“文档网格”与Word原生文档的文档网格大小无法相同是因为`styles.xml`文件**
    - 可以考虑新建一个原生文档，把所有用到的样式全部覆盖进去
  - 通过域代码实现页眉左上角参数自定义，原理为自定义meta data然后写入xml中引用
  - 适配“图表目录”标题
  - 增加了图目录
  - 通过修改reference.docx解决了页眉右上角标题的加粗问题
- 2021.04.24
  - 增加产生空格的函数来使“摘要”中间生成数个空格
  - 拆分插件到单独的仓库，改名
  - [X] ★对编号列表中的项目编号进行引用
  - 自定义图片的前缀后缀
  - [X] 图目录，表目录
- 2021.04.25
  - 修改模版文档，增加`singlePage`参数，为1表示单面打印
  - 因为修改页眉页脚造成rId变动，重写所有页眉页脚的rId值
  - 修正head.md中的bug
  - **在文档中对页眉页脚的机制做了相关说明**
  - **通过域代码，实现了单面双面打印的页眉页脚问题**
    - **单面打印/双面打印**
      - 需要制作两个模版……
      - 只做一个然后让用户自己看着办？
    - [X] 双面打印的页眉页脚设计
- 2021.04.26
  - 修复脚注编号功能
  - 重新适配页眉页脚rId值
  - ~~修改metadata参数更好预览~~，性能问题，去掉
  - 对兼容性问题增加说明
  - 修正模版的编号样式后缀和目录样式的对齐方式
- 2021.05.08
  - 讨论完成了定理环境的语法设计，代码还没写，样式还没做
  - 讨论完成了文档结构组织方式，LaTeX用户可以用类似的语法来调用
  - [X] 附录的二级标题及其编号如何实现？
    - 单独定义了附录二级标题的样式以及编号
    - 通过代码来修改附录的二级标题套用的样式解决附录编号问题
    - 通过代码单独对附录的题注使用不一样的域代码即可实现附录的题注编号
- 2021.05.09
  - 尝试寻找方式直接用同一份域代码实现页眉页脚，无果
    - 要么手动定义书签，要么通过固定的节号来实现对“目录”所在节的指定
    - 可以在metadata中写入“目录”所在的节号
  - 尝试通过Word的查找替换功能来实现页码的字号修改，~~无果~~解决！
    - ~~无法在目录查找到类似“\数字\回车符”这样的标记，应该是域中的特殊环境阻断了搜索~~
    - 生成目录时，如果域代码中带有`\h`参数，即“让生成的目录带有超链接”，此时目录中的标题会被应用“超链接”的文本样式，而中间的分隔符和页码为“默认段落字体”的文本样式
    - 于是可以通过带样式的查找替换完成
  - [X] 增加了对代码行号的显示功能

## 第一阶段

### 项目TODO

- [ ] ★该加入表格了
- [ ] ★拆分交叉引用的设定，使模块先具有通用性，并发布收集反馈
- [ ] 优化另一仓库中的readme，给出效果，拆分当前readme文件
- [ ] 重写交叉引用文档
- [ ] ★反馈pandoc的bug
  - [X] 换行符问题
  - [ ] 网格线显示问题：在研究公式行距问题过程中，发现pandoc输出的文档无法显示“网格线”，经查是`styles.xml`文件中部分内容与常规文档有所区别，具体xml内容后期整理并提交issue
  - [ ] 含有公式的表格公式对齐问题：设置表格内容居中，公式居中，结果公式位置偏右，经查是`settings.xml`中部分设置与pandoc表格所用的ooxml代码有关，后续提issue等pandoc解决
  - [ ] 建议保留`settings.xml`文件设定
    - 里面还涉及到公式字体等问题
- [ ] 拆分项目的更新日志到另一仓库
- [ ] 增加参数开关，把代码中的空格显示为`&blank;`，即“&blank;”`␣`

### 模版TODO

- [ ] 封面
- [ ] 定理环境样式设计
- [ ] 修改标题样式，使“段前段后”一行的效果与word匹配
- [ ] 允许在西文单词中间断字，以增强“超链接”的显示效果

### 代码TODO

可以单独实现

- [ ] ★通过metadata传参设置题注的语法
- [ ] ★附录的二级标题编号和题注编号
- [ ] ★定理环境实现
- [ ] 公式保留tex代码（不渲染）
  - 因为有的公式Word无法实现，需要调用其他工具生成
- [ ] 动态获取rId

## 第二阶段

### 项目TODO

- [ ] 兼容panbook的写法，借用其中的子图等写法
- [ ] 子图如何处理，能否提供接口实现按照页面比例创建表格而后插入图片？

  ```markdown
  ![xxx]()
  ![xxx]()
  ![xxx]()
  {30, 40, 30}
  ```

### 模版 TODO

- 表格图片前后一行
- [ ] 图片表格行距问题
  - 段前段后空一行的行距问题
    - 强行提高倍数拉高？
    - 在代码中增加空行？

---

- 目录相关
  - 索引
  - 术语表
- 尾注（英语专业需要）
- 表格样式能否实现？？
  - 普通表格的样式问题
  - 简单的三线表能否通过套样式实现？
- 标题编号的制表符与目录的位置微调（更好看）（低优先级）

### 文档TODO

- 编写《给小白的排版指导》，根据同学的不好的排版文档给出相应的指导和正确写法
- [ ] Word模版的文档，分两部分
  - （本科检查不严格，全部按研究生办）
  - 《给小白的Word排版思维指导》
    - 介绍排版思维，比如“样式”“分节符”
  - 《模版使用说明》
    - 介绍模版是如何实现排版要求的
    - 具体做了哪些工作，如何排版出来
- 目前的`template.md`作为模块的使用说明如何？
  - [ ] 记得写出交叉引用用的是自己的书签，而Word里用的是Word生成出来的标签

---

- 本科研究生的区别
  - 目前按照研究生标准处理页眉字号（当本科是打错字了）
  - 按研究生处理目录字体
  - 按研究生处理编号字体
- 编写《pandoc的妙用》？？（暂不考虑，低优先级）
  - 批量插入图片得到Word
    - 使用`ls`或者`dir`命令生成图片的路径，然后使用竖向的文本编辑生成图片格式插入到Markdown中转换

## 无法实现

- 表格目前无法合并单元格，等后期提issue然后pandoc更新
  - 可以通过插入域代码引入外部Word文件实现`{IncludeText xxxx}`
- 对于列表嵌套配合正文样式缩进什么的效果之后可能看起来会很奇怪，但是没有办法调整pandoc自带的编号层级，所以目前无法实现
- 脚注中的代码块会使用正文的代码字号，无法使用不同的字号（要求脚注小五，实际代码块五号）
  - 可以考虑定义脚注中的代码块样式，然后对其增加判断功能，目前暂不考虑
- 参考文献的英文多作者要求使用`et al`而非`等`，修改csl文件？
  - 经查证，似乎csl语言不支持这样的写法，因为无法判断中文文献和英文文献的标准？

### 可以通过后处理脚本实现

- 脚注的分隔线和其他设置
  - 脚注的分隔线缩进定义在`footnotes.xml`中，pandoc并不保留这个文件
  - 这玩意无解，只能最后导出之后用户手动调整
  - 一种思路是，在指定文件夹内保留相应的xml文件，处理完之后解压文档替换xml
- 四级标题编号的带圈序号实现（等上面那个调好了再说）

  ```xml
      <w:lvl w:ilvl="3">
        <w:start w:val="1"/>
        <w:numFmt w:val="decimalEnclosedCircleChinese"/>
        <w:lvlText w:val="%4"/>
        <w:lvlJc w:val="left"/>
        <w:pPr>
            <w:ind w:left="0" w:firstLine="0"/>
        </w:pPr>
      </w:lvl>
  ```
