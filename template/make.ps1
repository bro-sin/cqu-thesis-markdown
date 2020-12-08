pandoc.exe `
    .\template.md `
    -o .\template.docx `
    --filter ..\header_convert.py `
    --filter ..\equations_no.py `
    --filter ..\figures_no.py `
    --filter ..\refs.py `
    --filter ..\texcommands.py `
    --citeproc `
    --reference-doc .\reference.docx
    # --filter ..\section_break.py `
    # --toc `

start .\template.docx
