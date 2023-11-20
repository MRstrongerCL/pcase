# coding: utf-8
from .excelOperation import excel_opera
from .zhengjiao import generate_case_options

class CaseCreate(object):
    def __init__(self):
        self.case_template = {}

    def build_case_template(self,  define_case:dict=None, case_name='default_case', pre_condition='', steps='', expected='', case_class='', case_type='', priority='P3', module='', tag="", backup=""):
        """设定用例模板  (后面将用 {参数名称} 的方式 替换 成真正用例)
        :param define_case: dict 完全自定义用例模板，包括自定义title。（此参数有定义时，其他参数不生效）
        :param case_name: 用例名称
        :param steps: 用例步骤描述
        :param expected: 预期结果
        :param case_class: 所属测试集
        :param case_type: 用例类型
        :param module: 所属模块
        :param priority: 用例等级、优先级 P0 - P4
        :param pre_condition: 前置条件
        :param tag: 标签
        :param backup: 备注
        """
        if not define_case:
            self.case_template = {
                "用例名称": case_name,
                "所属测试集": case_class,
                "用例类型": case_type,
                "用例等级": priority,
                "前置条件": pre_condition,
                "步骤描述": steps,
                "预期结果": expected,
                "所属模块": module,
                "标签": tag,
                "备注": backup,
            }
        else:
            self.case_template = define_case
        return self.case_template

    def generate_group(self, *factors, ctype=1, csvt=False, print_status=False):
        """通过正交设计或全量组合生成 不同因素组合
        :param factors: 各因素列表，有2种形式
            第1种是只包含因素水平，如： ['标准-全局与计算', '标准-仅计算', "融合-全局与计算"]
            第2种是包含了因素水平和优先级，如：[('标准-全局与计算', 1), ('标准-仅计算', 2), ("融合-全局与计算", 3)]
        :param ctype: 计算方式 1、2、3、4
            1 - 各因素之间完全独立，且每个因素取值改变不会影响其他因素的测试结果，采用最小组合数方法，总体而言包含了各因素的各组合即可
            2 - 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最小行数选取正交表，可能存在某个因素的某个选项缺失的情况
            3 - 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最适合行数选取正交表，用例组合相对全面
            4 - 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用全量组合，用例组合完全覆盖
        :param csvt: 是否输出组合到csv，默认False
        :param print_status: 是否打印组合，默认False
        :return:
            cases_info list: [{"group": list_1, "priority": int_1},{"group": list_2, "priority": int_2},]
        """
        cases_info = generate_case_options(*factors, ctype=ctype, csvt=csvt, print_status=print_status)
        return cases_info

    def assemble_case(self, **kwargs):
        """生成用例, 将用例模板中的 {参数名称} 替换成 目标字符串
        :param **kwargs: 参数名称1: 值1, 参数名称2: 值2
        """
        truly_case = {}
        for title, source_str in self.case_template.items():
            new_tile = title
            target_str = source_str
            if target_str and target_str != '':
                for p,v in kwargs.items():
                    new_tile = new_tile.replace('{%s}' % p, str(v))
                    target_str = target_str.replace('{%s}' % p, str(v))
            truly_case[new_tile] = target_str
        return truly_case

    def assemble_cases(self, params: list, print_status=False):
        """批量产生用例
        :param params: list [ dict{} ] 用例参数集体，用于批量替换模板中{参数名称}，生成用例
        """
        cases = []
        for pa in params:
            case = self.assemble_case(**pa)
            cases.append(case)
            if print_status:
                print(case)
        return cases

    def WriteCase2Excel(self, epath, case_list, sname='cases1'):
        eo = excel_opera(excel_path=epath, type='write')
        eo.write(rows_list=case_list, sheet_name=sname)
        eo.save()

def sample_test():
    # 通过正交设计 生成用例组合
    input1_list = ['标准-全局与计算', '标准-仅计算', "融合-全局与计算"]
    input1_list = [('标准-全局与计算', 0), ('标准-仅计算', 2), ("融合-全局与计算", 1)]
    input2_list = ['SDN-3.0-POC', 'SDN-2.0-POC', 'VLAN-POC', 'SDN-3.0-常规', 'VLAN-常规']
    input2_list = [('SDN-3.0-POC', 1), ('SDN-2.0-POC', 3), ('VLAN-POC', 4), ('SDN-3.0-常规', 0), ('VLAN-常规', 2)]
    input3_list = ['repl', 'sanc', 'pair', 'local', 'tpsc']
    input4_list = ['2个管理节点', '3个管理节点', '4个管理节点']
    input_factors = [input1_list, input2_list, input3_list, input4_list]
    ca = CaseCreate()
    cases_info = ca.generate_group(*input_factors, ctype=1, csvt=False)

    # 生成用例c
    case_name = '验证典型配置全链路安装【{title}】'
    pre_condition = """1.安装环境已准备充分 \r\n2. 物理硬件、网络配置服务部署安装需求"""
    steps = """1.webinstaller配置为{group} \r\n2.点击安装，观察安装过程 \r\n3.检查安装结果，检查配置、服务"""
    expected = '3.配置一致；部署成功；服务正常'
    case_class = '/webinstaller/一期/全链路安装'
    case_type = '系统测试'
    priority = 'P3'
    # 设置用例模板
    ca.build_case_template(case_name=case_name, pre_condition=pre_condition, steps=steps, expected=expected,
                           case_class=case_class, case_type=case_type, priority=priority)
    # 替换模板中变量，生成可执行用例
    i = 1
    cases_params = []
    for case in cases_info:
        cgroup = case['group']
        title = f"{cgroup[0]}-{i}"
        priority = f"P{case['priority']}"
        cases_params.append({'title': title, 'group': cgroup, 'priority': priority})
        i += 1
    cases = ca.assemble_cases(cases_params)
    # 写入excel表中
    ca.WriteCase2Excel(epath='hacases.xlsx', case_list=cases)

if __name__ == '__main__':
    sample_test()