from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS

# class BookForm(forms.Form):
#     title = forms.CharField(max_length=32,label='书名')
#     price = forms.DecimalField(max_digits=8,decimal_places=2,label='价格')
#     date = forms.DateField(label='日期',
#         widget=widgets.TextInput(attrs={'type':'date'})
#     )
#     publish = forms.ModelChoiceField(queryset=models.Publish.objects.all(),label="出版社")
#     author = forms.ModelMultipleChoiceField(queryset=models.Author.objects.all(),label="作者")
#


class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = '__all__'
        widgets = {
            'date':widgets.TextInput(attrs={'type':'date','class':'form-control'}),
            'price':widgets.TextInput(attrs={'class':'form-control'}),
            'publish':widgets.Select(attrs={'class':'form-control'}),
            'title':widgets.TextInput(attrs={'class':'form-control'}),
            'authors':widgets.SelectMultiple(attrs={'class':'form-control'}),
        }
        labels = {
            'date':'日期',
            'title':'书名',
            'price':'价格',
            'publish':'出版社',
            'authors':'作者'
        }
        error_messages = {
            'title': {
                'required': ('不能为空'),
                'min_length': ('不能少于3位'),
                'max_length': ('不能大于5位'),
            },
            'price': {
                'invalid': '格式不正确',
                'required': ('不能为空'),
            }

        }



def books(request):

    book_list = models.Book.objects.all()
    return render(request,'books.html',{'book_list':book_list})


def book_add(request):

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/book/')

        #     title= form.cleaned_data.get('title')
        #     price = form.cleaned_data.get('price')
        #     date= form.cleaned_data.get('date')
        #     publish = form.cleaned_data.get('publish')
        #     author = form.cleaned_data.get('author')
        #
        #     book_obj = models.Book.objects.create(
        #     title = title,
        #     price = price,
        #     date = date,
        #     publish = publish
        # )
        #     book_obj.authors.add(*author)
        else:
            print(form.error_class)
            return render(request, 'add_book.html', locals())

    if request.method == 'GET':
        form = BookForm()
        return render(request,'add_book.html',locals())


def book_edit(request,id):
    # if request.method == 'POST':
    #     edit_obj = models.Book.objects.filter(id=id).first()
    #     publish_list = models.Publish.objects.all()
    #     author_list = models.Author.objects.all()
    #
    #     title = request.POST.get('title')
    #     price = request.POST.get('price')
    #     date = request.POST.get('date')
    #     publish_id = request.POST.get('publish_id')
    #     author_id_list = request.POST.getlist('author_id_list')
    #     models.Book.objects.filter(id=id).update(
    #         title=title,
    #         price=price,
    #         date=date,
    #         publish_id=publish_id,
    #     )
    #
    #     book_obj = models.Book.objects.filter(id=id).first()
    #     book_obj.authors.set(author_id_list)
    #     return redirect('/book/')

    if request.method == 'POST':
        edit_obj = models.Book.objects.filter(id=id).first() #要对谁进行update
        form = BookForm(request.POST,instance=edit_obj)#这是一个update操作
        if form.is_valid():
            form.save()
            return redirect('/book/')
    edit_obj = models.Book.objects.filter(id=id).first()
    form = BookForm(instance=edit_obj)
    return render(request,'edit_book.html',locals())



