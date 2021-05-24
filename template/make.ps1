# ת���ű�
$target = "template" # ת�����ļ��ļ���
$isOpenDocxAfterComplete = 1 # ת������Ƿ���Ҫ�Զ���
$coverName = "���Ʒ���"

$in = $target + ".md"
$out = $target + ".docx"
$coverFile = $coverName + ".md"

# ���������水��˳����Ӷ���ļ����ᰴ��˳��ϲ���һ��ʵ�ֶ��ĵ���֯�ṹ
# ����Ĭ�����ɡ�head.md���������$target�ļ��ϲ��õ���
pandoc.exe `
    head.md `
    $coverFile `
    $in `
    -o $out `
    --filter pandoc_word_helper `
    --citeproc `
    --metadata link-citations=true `
    --reference-doc .\reference.docx

if ($isOpenDocxAfterComplete) {
    Start-Process $out
}
