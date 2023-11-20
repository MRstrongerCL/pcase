# pcase

测试用例生成工具

# 功能简介
1. 各因素之间完全独立，且每个因素取值改变不会影响其他因素的测试结果，采用最小组合数方法，总体而言包含了各因素的各组合即可
2. 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最小行数选取正交表，可能存在某个因素的某个选项缺失的情况
3. 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最适合行数选取正交表，用例组合相对全面
4. 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用全量组合，用例组合完全覆盖

# Sample
from pcase.caseCreate import CaseCreate

## 定义不同因素的多个选项
input1_list = ['标准-全局与计算', '标准-仅计算', "融合-全局与计算"]
input1_list = [('标准-全局与计算', 0), ('标准-仅计算', 2), ("融合-全局与计算", 1)]
input2_list = ['SDN-3.0-POC', 'SDN-2.0-POC', 'VLAN-POC', 'SDN-3.0-常规', 'VLAN-常规']
input2_list = [('SDN-3.0-POC', 1), ('SDN-2.0-POC', 3), ('VLAN-POC', 4), ('SDN-3.0-常规', 0), ('VLAN-常规', 2)]
input3_list = ['repl', 'sanc', 'pair', 'local', 'tpsc']
input4_list = ['2个管理节点', '3个管理节点', '4个管理节点']
input_factors = [input1_list, input2_list, input3_list, input4_list]

## 初始化实例
ca = CaseCreate()
## 产生不同组合
cases_info = ca.generate_group(*input_factors, ctype=3, csvt=False, print_status=True)
## 定义用例模板
case_temple = {
    '用例名称': '验证典型配置全链路安装【{title}】',
    '前置条件': '1.安装环境已准备充分 \r\n2. 物理硬件、网络配置服务部署安装需求 \r\n3. 已拉起fb，并成功登录webinstaller',
    '用例步骤': '1.webinstaller配置为{group} \r\n2.点击安装，观察安装过程 \r\n3.检查安装结果，检查配置、服务',
    '预期结果': '3.配置一致；部署成功；服务正常',
    '优先级': '{priority}'
}
ca.build_case_template(define_case=case_temple)
## 替换模板中参数，生成实际用例
cases_params = []
for case in cases_info:
    case_params = {
        'group': case['group'],
        'title': '+'.join(case['group'][:3]),
        'priority': f'P{case["priority"]}',
    }
    cases_params.append(case_params)
cases = ca.assemble_cases(params=cases_params, print_status=True)
## 用例写入excel
ca.WriteCase2Excel(epath='hacases.xlsx', case_list=cases)
