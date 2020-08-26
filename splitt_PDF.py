from PyPDF2 import PdfFileReader, PdfFileWriter
import os, time, sys

def split_pdf(in_filename, outpath):
    """
    split a pdf into several pdf and output in a created inventory with the name of file pdf
    :param infn:
    :param outpath:
    :return:
    """
    pdf_name = os.path.basename(in_filename)
    inventory_name = pdf_name.replace('.pdf', '')
    inventory_path = outpath + inventory_name

    try:
        os.mkdir(inventory_path)
    except FileExistsError:
        print('Directory existed!')
    else:
        print('Directory created successfully')

    pdf_input = PdfFileReader(open(in_filename, 'rb'))
    # 获取 pdf 共用多少页
    page_count = pdf_input.getNumPages()
    print('total page =', page_count)
    # 将 pdf 第五页之后的页面，输出到一个新的文件
    for i in range(page_count):
        pdf_output = PdfFileWriter()
        pdf_output.addPage(pdf_input.getPage(i))
        # i += 1
        if i < 9:
            index = '00' + str(i+1)
        elif i >= 9 and i < 99:
            index = '0' + str(i + 1)
        elif i >= 100:
            index = i
        pdf_output.write(open(inventory_path + '/' + inventory_name + '_page_{}.pdf'.format(index), 'wb'))

    print('spilting succeeded!')

def merge_pdf(inputpath, outputpath):
    """
    merge several pdf in a given inventory and store the merged pdf in output path

    :param inputpath: input inventory path
    :param outfn: output path
    :return: merged file path
    """
    dirlist = os.listdir(inputpath)
    pdf_output = PdfFileWriter()
    for infn in dirlist:
        pdf_input = PdfFileReader(open(inputpath + infn, 'rb'))
        # 获取 pdf 共用多少页
        page_count = pdf_input.getNumPages()
        # print(page_count)
        for i in range(page_count):
            pdf_output.addPage(pdf_input.getPage(i))

    time_stamp = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filepath = outputpath + 'merged_pdf_{}.pdf'.format(int(time_stamp))
    pdf_output.write(open(filepath, 'wb'))
    print('merged succeeded!')
    return filepath

def compress_pdf(input_filepath, outputpath):
    """
    input a file path and compress the pdf file, output the compressed pdf in given path
    :param input_filepath:
    :param outputpath:
    :return:
    """
    if ' ' in input_filepath:
        print('Warning:too many space in filename, must rename the file with no space in name!')
        sys.exit(1)

    file_name = os.path.basename(input_filepath).replace('.pdf', '')
    file_name = os.path.basename(file_name).replace(' ', '')

    compress_name = outputpath + file_name + '_compressed.pdf'

    sys.path.append('C:/pdfsizeopt')
    os.chdir('C:/pdfsizeopt')
    cmd = 'C:/pdfsizeopt/pdfsizeopt'+' '+ input_filepath+' '+ compress_name
    os.system(cmd)
    print('compressed succeeded!')

if __name__ == '__main__':

    name = 'skript-linearantriebe-2013-scan-farbig.pdf'
    input_path = os.path.normpath("C:/Users/53276/Desktop/" + name)
    output_path = "C:/Users/53276/Desktop/"

    path2 = input_path.replace('.pdf','') + '/'
    # split_pdf(input_path, output_path)
    path3 = merge_pdf(path2, output_path)
    # print(path3)
    compress_pdf(path3, output_path)

