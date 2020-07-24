from django import forms

class UserForm(forms.Form):
    GENDERS = (
        ('male', '男性'),
        ('female', '女性'),
        ('unknown', '未知'),
    )
    name = forms.CharField(max_length=10)
    birth = forms.DateField()
    bio = forms.FloatField()
    # 这里需要用 ChoiceField
    gender = forms.ChoiceField(choices=GENDERS)


# nickname:34143312
# birthday:2000-01-01
# gender:male
# location:广州
# dating_gender:male
# dating_location:上海
# max_distance:100
# min_distance:200
# max_dating_age:19
# min_dating_age:10
# vibration:False
# only_matched:True
# auto_play:True
