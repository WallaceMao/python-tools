import os
from pdf2image import convert_from_path

poppler_path = './lib/poppler-22.04.0/Library/bin'
origin_extend = ".pdf"
target_extend = ".png"


def convert_single(p_input_file_without_ext, p_output_file_without_ext):
    p_input_file = p_input_file_without_ext + origin_extend
    images = convert_from_path(p_input_file, poppler_path=poppler_path)
    for index, image in enumerate(images):
        suffix = ""
        if index != 0:
            suffix = "__{}".format(str(index))
        final_file_name = p_output_file_without_ext + suffix + target_extend
        image.save(final_file_name)
        print("====> {} --> {}".format(p_input_file, final_file_name))


def find_pdf_and_convert(p_input_folder, p_output_folder):
    directory = os.fsencode(p_input_folder)

    print("==> 开始转换：{} ==> {}".format(p_input_folder, p_output_folder))
    print("==> 格式：{} ==> {}".format(origin_extend, target_extend))

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(origin_extend):
            convert_single(
                os.path.join(p_input_folder, filename[:-len(origin_extend)]),
                os.path.join(p_output_folder, filename[:-len(origin_extend)]))
            continue
        else:
            continue

    print("==> 完成转换")


if __name__ == '__main__':
    input_folder = "./input"
    output_folder = "./output"
    find_pdf_and_convert(input_folder, output_folder)
