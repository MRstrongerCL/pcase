# -- coding:utf-8 --
# chenliang
# 2022-12-29
# desc: excel文件处理

import xlrd,xlwt

class excel_opera():
    """excel文件读写"""

    def __init__(self, excel_path, type='read'):
        """初始化
        :param excel_path: excel文件路径
        :param type： 读、写， read、write
        """
        self.excel_path = excel_path
        self.init_book(type)

    def init_book(self, type='read'):
        if type == "write":
            self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        else:
            self.book = xlrd.open_workbook(self.excel_path)

    def read_2list(self, sheet_key=0, readRows=None):
        # 读
        print(f"... ready to read {self.excel_path}")
        try:
            sheet_key = int(sheet_key)
            sheet = self.book.sheet_by_index(sheet_key)
        except:
            sheet = self.book.sheet_by_name(sheet_key)
        nrows = sheet.nrows
        ncols = sheet.ncols
        titles = sheet.row_values(0)
        if readRows is None or readRows == 0:
            endRows = nrows
        else:
            try:
                endRows = int(readRows)
            except:
                endRows = nrows
        return_list = []
        for i in range(endRows)[1:]:
            values = sheet.row_values(i)
            line_dict = dict(zip(titles, values))
            return_list.append(line_dict)
            # print(line_dict)
        print(f"... read success {self.excel_path}")
        return return_list

    def write(self, rows_list, sheet_name='new'):
        print(f"... ready to write {self.excel_path} sheet: {sheet_name}")
        sheetw = self.book.add_sheet(sheet_name, cell_overwrite_ok=True)  # 其中的new是这张表的名字
        if rows_list == []:
            print("... have no input datas , don't need write")
            return
        line1 = rows_list[0]
        title_index = {}
        index = 0
        # 写标题栏
        for title in line1.keys():
            sheetw.write(0, index, title)
            title_index.setdefault(title, index)
            index += 1
        # 写数据栏
        # style = xlwt.XFStyle()
        # style.alignment.wrap = 1  # 设置自动换行

        row_no = 1
        for line in rows_list:
            for title, value in line.items():
                index = title_index[title]
                # sheetw.write(row_no, index, value, style)
                sheetw.write(row_no, index, value)
            row_no += 1

    def save(self):
        self.book.save(self.excel_path)
        print(f"... save success {self.excel_path}")

def writeExcel_f_list(excel_path, rows_list, sheet_name='new'):
    """写excel，根据列表格式，每个元素都是字典
    :param sheet_key: sheet名称str 或者 索引int
    """
    # 写
    print(f"... ready to write {excel_path} sheet: {sheet_name}")
    bookw = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheetw = bookw.add_sheet(sheet_name, cell_overwrite_ok=True)  # 其中的new是这张表的名字
    line1 = rows_list[0]
    title_index = {}
    index = 0
    # 写标题栏
    for title in line1.keys():
        sheetw.write(0,index,title)
        title_index.setdefault(title, index)
        index += 1
    # 写数据栏
    # style = xlwt.XFStyle()
    # style.alignment.wrap = 1  # 设置自动换行

    row_no = 1
    for line in rows_list:
        for title,value in line.items():
            index = title_index[title]
            # sheetw.write(row_no, index, value, style)
            sheetw.write(row_no, index, value)
        row_no += 1
    bookw.save(excel_path)
    print(f"... write success {excel_path} sheet: {sheet_name}")


def readExcel_2_list(excel_path, sheet_key, readRows=None):
    """读取excel，返回列表格式，每个元素都是字典
    :param sheet_key: sheet名称str 或者 索引int
    """
    # 读
    print(f"... ready to read {excel_path}")
    book = xlrd.open_workbook(excel_path)
    try:
        sheet_key = int(sheet_key)
        sheet = book.sheet_by_index(sheet_key)
    except:
        sheet = book.sheet_by_name(sheet_key)
    nrows = sheet.nrows
    ncols = sheet.ncols
    titles = sheet.row_values(0)
    if readRows is None or readRows == 0:
        endRows = nrows
    else:
        try:
            endRows = int(readRows)
        except:
            endRows = nrows
    return_list = []
    for i in range(endRows)[1:]:
        values = sheet.row_values(i)
        line_dict = dict(zip(titles,values))
        return_list.append(line_dict)
        # print(line_dict)
    print(f"... read success {excel_path}")
    return return_list

def product_source_case(excel_data:list) -> list:
    """根据生成用例需要生成原始数据
    :param excel_data: 从用例excel中读取的数据
    """

if __name__ == '__main__':
    epath='sanc用例.xls'
    re = readExcel_2_list(excel_path=epath, sheet_key='zookeeper', readRows=5)
    writeExcel_f_list("new.xls", rows_list=re)