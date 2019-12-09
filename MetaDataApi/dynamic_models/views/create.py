from django.shortcuts import render

from MetaDataApi.dynamic_models.forms import CreateRequestForm


def create_models_from_json_view(request):
    if request.method == "POST":
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            create_request = form.save(commit=False)
            create_request.status = 0
            create_request.save()
            # return redirect('post_detail', pk=create_request.pk)
    else:
        form = CreateRequestForm()
    return render(request, 'create_models_from_json.html', {'form': form})
