# from dex2c.writer import TmpnameAllocator
#
#
# class FakeField:
#     """模拟 ins.get_field() 返回的对象。
#     两个 name 相同、ftype 不同的对象——如果 __eq__/__hash__
#     只看 name，它们就会被判相等。"""
#
#     def __init__(self, name, ftype):
#         self.name = name
#         self.ftype = ftype
#
#     def __repr__(self):
#         # 故意只打印 name，模拟"看起来一样"
#         return f"Field({self.name!r})"
#
#     def __eq__(self, other):
#         # 只比较 name（这就是可能的 bug 源头）
#         return isinstance(other, FakeField) and self.name == other.name
#
#     def __hash__(self):
#         return hash(self.name)
#
#     def get_field(self):
#         # 用 type 一起拼 key
#         return '%s.%s' % (self.name, self.ftype)   # 简化版，只要含 type 就行
#
# f_obj = FakeField("ʻ...ʼ", "Ljava/lang/Object;")
# f_str = FakeField("ʻ...ʼ", "Ljava/lang/String;")
#
# print("f_obj == f_str :", f_obj == f_str)         # True 有 bug
# print("hash 相等      :", hash(f_obj) == hash(f_str))
#
# # 跑一遍分配器
# fa = TmpnameAllocator([f_obj, f_str], "ifld").get_name
# print("f_obj ->", fa(f_obj))
# print("f_str ->", fa(f_str))
# print(f_obj.get_field() == f_str.get_field())
# # 若两行输出相同（如 ifld0），说明 TmpnameAllocator 会把它们合并确诊




# import os, sys
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
#
# from dex2c.compiler import auto_vm
# from androguard.core.analysis import analysis
# from androguard.core.bytecodes import apk, dvm
# from androguard.util import read
# from collections import Counter
# import androguard.core.androconf as androconf
# from dex2c.compiler import Dex2C
# from dex2c.compiler import IrBuilder
#
#
# class FakeVMX:
#     """把 Analysis 包装成只有 get_method 的接口"""
#     def __init__(self, vma):
#         self.vma = vma
#     def get_method(self, m):
#         return self.vma.get_method(m)
#
#
# def scan(apk_path):
#     vm = auto_vm(apk_path)
#     vma = analysis.Analysis(vm)
#     vmx = FakeVMX(vma)
#
#     all_fields = []
#     all_methods = []
#
#     for dvclass in vm.get_classes():
#         for m in dvclass.get_methods():
#             if m.get_code() is None:
#                 continue
#             try:
#                 mx = vma.get_method(m)
#                 builder = IrBuilder(mx)
#                 irmethod = builder.process()
#                 if irmethod is None:
#                     continue
#                 entry = irmethod.entry
#                 all_fields.extend(entry.field_to_declare)
#                 all_methods.extend(entry.method_to_declare)
#             except Exception as e:
#                 # 处理不了的方法跳过
#                 pass
#
#     # 字段：按 (repr) 找重复 key，并打印它们的完整信息
#     print("=" * 60)
#     print(f"共收集 {len(all_fields)} 个字段引用, {len(all_methods)} 个方法引用")
#
#     fc = Counter(repr(f) for f in all_fields)
#     dupes = {k: v for k, v in fc.items() if v > 1}
#     print(f"\n字段: {len(dupes)} 组 repr 重复")
#     for k, v in sorted(dupes.items(), key=lambda x: -x[1])[:30]:
#         hits = [x for x in all_fields if repr(x) == k]
#         types = set(getattr(x, 'field_type', None) or getattr(x, 'ftype', None) or '?' for x in hits)
#         eq_pairs = [(i, j) for i in range(len(hits)) for j in range(i+1, len(hits))
#                     if hits[i] == hits[j] and hits[i] is not hits[j]]
#         print(f"  x{v}  {k}")
#         for h in hits[:5]:
#             print(f"      {h!r}  hash={hash(h)}  id={id(h)}")
#
#     mc = Counter(repr(m) for m in all_methods)
#     dupes_m = {k: v for k, v in mc.items() if v > 1}
#     print(f"\n方法: {len(dupes_m)} 组 repr 重复")
#     for k, v in sorted(dupes_m.items(), key=lambda x: -x[1])[:30]:
#         print(f"  x{v}  {k}")
#
#
# if __name__ == "__main__":
#     scan("\\".join(os.path.abspath(__file__).split("\\")[0:-2])+ "\\app\\" + "test.apk")



# from dex2c.writer import TmpnameAllocator
#
# # 模拟"旧版 get_field()"的返回（只含 clsdesc + name）
# s1_old = "Lcom/xx/MainActivity;.ʻ...ʼ"
# s2_old = "Lcom/xx/MainActivity;.ʻ...ʼ"
# print("旧版 key 相等:", s1_old == s2_old)   # True → 会冲突
#
# # 模拟"新版 get_field()"的返回（拼上 ftype）
# s1_new = "Lcom/xx/MainActivity;.ʻ...ʼ:Ljava/lang/Object;"
# s2_new = "Lcom/xx/MainActivity;.ʻ...ʼ:Ljava/lang/String;"
# print("新版 key 相等:", s1_new == s2_new)   # False → 不会冲突
#
# fa = TmpnameAllocator([s1_new, s2_new], "ifld").get_name
# print("s1 ->", fa(s1_new))   # ifld0
# print("s2 ->", fa(s2_new))   # ifld1


# from dex2c.writer import TmpnameAllocator
# from dex2c.instruction import InstanceExpression, Variable
#
# cls = "Lcom/xx/MainActivity;"
# name = "ʻ...ʼ"
#
# # 两个 InstanceExpression，名字相同、ftype 不同
# v1 = Variable(0, 0); v1.set_type(cls)
# v2 = Variable(1, 0); v2.set_type(cls)
# r1 = Variable(2, 0); r1.set_type("Ljava/lang/Object;")
# r2 = Variable(3, 0); r2.set_type("Ljava/lang/String;")
#
# ie1 = InstanceExpression(r1, v1, cls, "Ljava/lang/Object;", name)
# ie2 = InstanceExpression(r2, v2, cls, "Ljava/lang/String;", name)
#
# print("ie1.get_field() =", ie1.get_field())
# print("ie2.get_field() =", ie2.get_field())
# print("相等:", ie1.get_field() == ie2.get_field())   # 改了之后应为 False
#
# fa = TmpnameAllocator([ie1.get_field(), ie2.get_field()], "ifld").get_name
# print("fa(ie1) =", fa(ie1.get_field()))   # ifld0
# print("fa(ie2) =", fa(ie2.get_field()))   # ifld1