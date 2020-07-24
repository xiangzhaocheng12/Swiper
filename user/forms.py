from django import forms

# 除了form, 还有一个 ModelForm
# 如果是从某一个模型里面直接搬过来的属性, 可以直接
from user.models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # fields 表示需要的属性
        fields = ['nickname','gender','birthday','location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # 把里面的所有属性都取出来
        fields = '__all__'

    # 处理 form 表单必须以  clean_ 作为开头 + 一个字段名
    def clean_max_distance(self):
        '''清洗最大距离'''
            # 注意:不能直接调用clean方法
        cleaned_data = super().clean()
        # 判断距离
        if cleaned_data['max_distance'] >= cleaned_data['min_distance']:
            return cleaned_data['max_distance']
        else:
            # ValidationError 为Django定义好的异常, 不会直接跑出来, 而是放在errors里面
            # Django会捕获这个异常, 并进行收集
            raise forms.ValidationError('最大距离必须大于等于最小距离')


    def clean_max_dating_age(self):
        '''清洗最大年龄'''
        cleaned_data = super().clean()
        # 判断距离
        if cleaned_data['max_dating_age'] >= cleaned_data['min_dating_age']:
            return cleaned_data['max_dating_age']
        else:
            # ValidationError 为Django定义好的异常, 不会直接跑出来, 而是放在errors里面
            # Django会捕获这个异常, 并进行收集
            raise forms.ValidationError('最大年龄必须大于等于最小年龄')