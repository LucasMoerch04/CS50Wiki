from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from django.urls import reverse
import markdown2
from django import forms

class NewForm(forms.Form):
    search = forms.CharField(label= "",max_length=100)

class ConfForm(forms.Form):
        title = forms.CharField(widget=forms.TextInput(attrs={'id':'textinput'}))
        content = forms.CharField(widget=forms.Textarea(attrs={'id':'textarea'}), label="Content:", initial="")

    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewForm()
    })
    
def get_page(request, title):
    page = util.get_entry(title)
    
    if page is None:
        return render(request, "encyclopedia/errorpage.html", {
            'title':title,
            "form": NewForm()
            })
    
    return render(request, "encyclopedia/page.html",{
        'title': title,
        "content": markdown2.markdown(page),
        "form": NewForm()
    })
    
def search(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
        
        query = query.lower()
        entries = util.list_entries()
        entries_lower = [x.lower() for x in entries]
        if query in entries_lower:
            return redirect('wiki:get_page', query)
        else:
            entries_like = []
            for s in entries_lower:
                index = s.find(query)
                if index >= 0:
                    entries_like.append(s)
            if entries_like:
                entry_titles = []
                for entry in entries:
                    for i in range(len(entries_like)):
                        if entries_like[i] == entry.lower():
                            entry_titles.append(entry)
                        
                found = True
                return render(request, "encyclopedia/results.html",{
                    "entries": entry_titles,
                    "query": query,
                    "found": found
                })
            else: 
                return render(request, "encyclopedia/results.html",{
                    "query": query,
                })
                    

def new(request):
    return render(request, "encyclopedia/conf/newpage.html", {
        "form": NewForm(),
        "confform": ConfForm()
    })
    
def new_save(request):
    if request.method == "POST":
        form = ConfForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            entries = util.list_entries()
            print(title, content)

            entries_lower = [x.lower() for x in entries]
            
            for entry in entries_lower:
                if title.lower() == entry:
                    TitleTaken = True
                    return render(request, "encyclopedia/errorpage.html", {
                        'title':title,
                        "form": NewForm(),
                        "saveError": TitleTaken
                        })
            
                
            print(title, content)
            util.save_entry(title, content)
            
            page = util.get_entry(title)
            return render(request, "encyclopedia/page.html",{
                'title': title,
                "content": markdown2.markdown(page),
                "form": NewForm()
            })
            
def edit(request, title):
    page = util.get_entry(title)
    conf_form = ConfForm(initial={'content': page, 'title': title})
    
    
    return render(request, "encyclopedia/editpage.html", {
        "page" : page,
        "form": NewForm(),
        "confform": conf_form,
        'title': title,
        "content": markdown2.markdown(page),
    })
    
def edit_save(request):
    if request.method == "POST":
        form = ConfForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            util.save_entry(title, content)
            
            page = util.get_entry(title)
            return render(request, "encyclopedia/page.html",{
                'title': title,
                "content": markdown2.markdown(page),
                "form": NewForm()
            })