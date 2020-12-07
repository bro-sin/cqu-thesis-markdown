## 运行

```text
pandoc example.md  --filter equations_no.py --filter section_break.py --filter header_convert.py -o example.docx
```

## 样式

除了 pandoc 预设的那几个样式外，还有以下几种特殊样式

- `TOC Heading`: 目录标题
- `Unnumbered Heading 1`: 无编号的一级标题
- `Unnumbered Heading 2`: 无编号的二级标题
- `Appendix Text`: 附录正文样式
- `Plain Text`: 无缩进的普通文本，用做公式编号的样式等
- `Heading Numbering`：标题的编号列表
- `Key Word`：“关键字”的前缀字符样式

## 命令定义

- `标题{-}`：后面的`{-}`表示去掉某标题的编号，根据排版要求和实现方案，仅提供一级标题（适用于摘要，附录，参考文献）和二级标题（适用于附录内部的二级标题`A`,`B`等）
- `附录{- .appendix}`：`{}`中的`-`表示去掉编号，`.appendix`表示该部分是目录。因为排版要求规定附录中的字号比正文小，所以需要单独标注出附录来为附录中的正文套用单独的附录样式（见`样式`章节）
  - 实现原理：单独定义了未编号的一级标题和二级标题样式（见`样式`部分）
- `\KeyWord{关键词1，关键词2}`和`\SecondKeyWord{keyword1, keyword2}`：产生中英文关键词前缀
  - 实现原理：单独定义中英文前缀的字符串内容然后套用预设的`KeyWord`文本样式
  - （为了通用性，可以自定义前缀以适用于其他语言，所以用SecondKeyWord做命令而未使用EnglishKeyWord）
- `\toc{目录}`：产生标题为`目录`的目录
- `\newSection{UpperRoman}`和`\newSection{Arabic}`：产生分节符，并设置对应节的页码为大写罗马数字或阿拉伯数字
  - 实现原理：通过文本匹配替换，直接插入对应的ooxml代码
  - 分节符的作用：控制**分节符位置前方**的页面的“页面参数”，例如纸张大小，分栏，**仅在不同的“节”中才能生成不同样式的页眉页脚**，所以为了实现不同的页眉页脚效果，必须插入分节符
- `\newLine{}`：插入换行符，在不分段的情况下进入下一行（即Word中`Shift` + `Enter`的效果），可用来产生双语题注
  - 实现原理：替换为ooxml代码或pandoc原生的`LineBreak`对象
- `\secondCaption{fig}`：插入双语题注的第二题注时，用该命令产生第二语言的编号前缀，例如中英题注中，默认会生成中文的题注编号`图1.3`，而英文题注的编号则须用该命令产生`Fig 1.3`
  - 实现原理：预设第二题注的前缀，插入域代码生成编号
- `\Reference{}`：在当前位置插入参考文献，因为排版要求规定`附录`在`参考文献`之后，而pandoc默认参考文献插入在文档最后，所以需要定义命令以在任意位置插入参考文献
- \`{some code}\`{=field}：`some code`为域代码，`{=field}`表示把该部分内容作为域代码处理，通过该语法可以实现插入自定义域代码的功能
- `[被标记文本]{#书签名字}`：可以对`被标记文本`标记一个名为`书签名字`的书签，通过书签和域代码配合，可以实现交叉引用。该功能为pandoc自带功能

## 开发日志

- 2020.12.05~2020.12.06：
  - 总结CQU排版要求{@ilcpm}
  - python变成实现[@Hagb]
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

## 模版TODO

- 内联代码样式
- 术语表
- 表目录图目录
- 封面
- 标题编号的制表符与目录的位置微调（更好看）
- 尾注
- 脚注的分隔线
- 四级标题编号的带圈序号（等上面那个调好了再说）

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

- 本科研究生的区别
  - 目前按照研究生标准处理页眉字号（当本科是打错字了）
  - 按研究生处理目录字体
  - 按研究生处理编号字体
  - （本科检查不严格，全部按研究生办）
- 页眉页脚如何处理？
