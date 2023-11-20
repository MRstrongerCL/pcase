# coding: utf-8
import random,csv
from pyDOE2 import lhs  # 标准正交表
from pyDOE2 import fullfact  # 全量组合
from .conf import standard  # 导入正交水平配置表

def samples_levels(levels):
    '''获取因素个数、水平数分布'''
    factor_count = 0
    target = {}
    for l in levels:
        if str(l) not in target.keys():
            c = levels.count(l)
            factor_count += c
            target[str(l)] = c
    return factor_count, target

def view_levels(tv):
    '''可视化水平数'''
    vtv = []
    for t,v in tv.items():
        vtv.append(f'{t}^{v}')
    return '.'.join(vtv)

def best_choice_n(levels, sample=True):
    '''{n: [{水平数: 因素个数}]}'''
    tc, target = samples_levels(levels)
    n = 1
    for l, c in target.items():
        n += (int(l) - 1) * c
    vtv = view_levels(target)
    if sample:
        return n, target
    for k,v in standard.items():
        ki = int(k)
        if ki < n:
            continue
        for group in v:
            # 比较正交表中 因素个数 少于 输入的因素个数 则不符合
            stc = 0
            for ssl, ssc in group.items():
                stc += ssc
            if stc < tc:
                continue
            # 判断水平数对应的因素个数是否符合需求
            status = True
            instead = {}
            for ll, cc in target.items():
                owne_count = group.get(str(ll), 0)
                if owne_count < cc:
                    status = False
                    # 如果没有查到对应水平数，则查询更大的水平数，此处并不完美
                    for sl, sc in group.items():
                        if int(sl) >= int(ll):
                            instead_count = instead.get(sl, 0)
                            if sc >= (cc + instead_count):
                                instead[sl] = cc + instead_count
                                status = True
                                break
                    if not status:
                        break
            if not status:
                continue
            else:
                return int(ki), group
    print(f'没有找到合适的行数n: {n} {levels}')

def generate_orthogonal_table(factors, ctype=2, print_status=False):
    '''生成正交试验表 (有瑕疵 并未对照标准的正交表 行数n不一定正确)'''
    facn = len(factors)
    levels = [len(factor) for factor in factors]
    print('输入因素水平数:', levels)
    if ctype == 2:
        n, group = best_choice_n(levels, sample=True)
        arrays = lhs(facn, n, criterion='maximin')
        print('正交试验最少行数:', n)
        print('选择因素分布:', view_levels(group))
    elif ctype == 3:
        n, group = best_choice_n(levels, sample=False)
        arrays = lhs(facn, n, criterion='maximin')
        print('正交试验最合适行数:', n)
        print('选择因素分布:', view_levels(group))
    else:
        n, group = samples_levels(levels)
        arrays = fullfact(levels)  # 全量
        print('全量组合行数:', len(arrays))
        print('因素分布:', view_levels(group))
    # print(f'选择正交表：L{len(arrays)}({view_levels(group)})')
    # for one in arrays:
    #     print(one)
    count = 1
    options_list = []
    for line in arrays:
        options = []
        priorities = []
        for i in range(len(line)):
            if ctype in [2, 3]:
                j = int(round(line[i] * (levels[i] - 1)))
            else:
                j = int(line[i])
            ops = factors[i][j]
            if type(ops) in [tuple, list]:
                options.append(ops[0])
                priorities.append(ops[1])
            else:
                options.append(ops)
                priorities.append(3)  # 未定义优先级，则默认为3
        priority = round(sum(priorities)/len(priorities))
        one_group = {'group': options, 'priority': priority}
        if one_group not in options_list:
            options_list.append(one_group)  # 排重
            if print_status:
                print(f"--> {count}", options, priority)
            count += 1
    return options_list

def generate_less_table(factors, print_status=False):
    '''采用最小组合数方法，总体而言包含了各因素的各组合即可
    :param factors: 因素列表
    '''
    levels = [len(factor) for factor in factors]
    tc, target = samples_levels(levels)
    vtv = view_levels(target)
    print('输入因素水平数:', vtv)
    maxl = max(levels)
    print('采用最小组合数方法n:', maxl)
    options_list = []
    for i in range(maxl):
        options = []
        priorities = []
        for factor in factors:
            if len(factor) > i:
                ops = factor[i]
            else:
                ops = random.choice(factor)
            if type(ops) in [tuple, list]:
                options.append(ops[0])
                priorities.append(ops[1])
            else:
                options.append(ops)
                priorities.append(3)  # 未定义优先级，则默认为3
        priority = round(sum(priorities)/len(priorities))
        one_group = {'group': options, 'priority': priority}
        if one_group not in options_list:
            options_list.append(one_group)  # 排重
            if print_status:
                print(f"--> {i+1}", options, priority)
    return options_list

def generate_case_options(*factors, ctype=1, csvt=False, print_status=False):
    """ 根据多个不同因素 组合用例
    Args:
        *factors: 各因素水平列表 factor1_list, factor2_list, factor3_list
            factor_list 有2种形式
            第1种是只包含因素水平，如： ['标准-全局与计算', '标准-仅计算', "融合-全局与计算"]
            第2种是包含了因素水平和优先级，如：[('标准-全局与计算', 1), ('标准-仅计算', 2), ("融合-全局与计算", 3)]
        ctype (int): 组合类型，共分为4种类型：1、2、3、4
            1 - 各因素之间完全独立，且每个因素取值改变不会影响其他因素的测试结果，采用最小组合数方法，总体而言包含了各因素的各组合即可
            2 - 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最小行数选取正交表，可能存在某个因素的某个选项缺失的情况
            3 - 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最适合行数选取正交表，用例组合相对全面
            4 - 各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用全量组合，用例组合完全覆盖
        csvt (bool): 是否输出到CSV文件中, True | False

    Returns:
        cases (list)
    """
    desc = {
        "1": "各因素之间完全独立，且每个因素取值改变不会影响其他因素的测试结果，采用最小组合数方法，总体而言包含了各因素的各组合即可",
        "2": "各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最小行数选取正交表，可能存在某个因素的某个选项缺失的情况",
        "3": "各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用正交试验设计，使用最适合行数选取正交表，用例组合相对全面",
        "4": "各因素之间完全独立，各个因素取值改变可能会影响其他因素的测试结果，采用全量组合，用例组合完全覆盖",
    }
    print(f'*** type: {ctype} ***\n{desc[str(ctype)]}\n***************')
    if ctype == 1:
        cases = generate_less_table(factors, print_status=print_status)
    else:
        cases = generate_orthogonal_table(factors, ctype=ctype, print_status=print_status)
    print('----------------------------------------------')
    print(f'完成组合, 排重后共计有效组合 {len(cases)} 个.')
    if csvt:
        fname = 'cases.csv'
        with open(fname, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(cases)
        print('已输出到csv文件:', fname)
    return cases

def infact_sample1():
    # 定义各个输入项的选项
    input1_list = [('标准-全局与计算', 1), ('标准-仅计算', 2), ("融合-全局与计算", 3)]
    input2_list = [('SDN-3.0-POC', 2), ('SDN-2.0-POC', 3), ('VLAN-POC', 4), ('SDN-3.0-常规', 1), ('VLAN-常规', 2)]
    input3_list = ['repl', 'sanc', 'pair', 'local', 'tpsc']
    input4_list = ['2个管理节点', '3个管理节点', '4个管理节点']
    input5_list = ['有服务组件ip范围', '无服务组件ip范围']
    input6_list = ['共用管理网络', '独立业务网络']
    input7_list = ['手动规划基础网络', '自动规划基础网络']
    input_factors = [input1_list, input2_list, input3_list, input4_list, input5_list, input6_list, input7_list]
    cases = generate_case_options(*input_factors, ctype=3, csvt=False, print_status=True)

if __name__ == '__main__':
    infact_sample1()