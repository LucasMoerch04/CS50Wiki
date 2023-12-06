from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from django.urls import reverse
import markdown2
from django import forms

class NewForm(forms.Form):
    search = forms.CharField(label= "",max_length=100)


    
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
                    
                    
