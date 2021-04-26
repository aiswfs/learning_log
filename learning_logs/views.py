from django.shortcuts import render,redirect
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.
def index(request):
	'''主页'''
	return render(request,'learning_logs/index.html')

@login_required
def topics(request):
	""""返回所有主题"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')

	# topics = Topic.objects.order_by('date_added')
	context = {'topics':topics}
	return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id): #URL模式
	""""返回所有主题"""
	topic = Topic.objects.get(id=topic_id)

	if topic.owner != request.owner:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic,'entries':entries}
	return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
	'''添加新主题'''
	if request.method != "POST":
		#post 未提交数据,展示空表单呗
		form = TopicForm()
	else:
		#等于post提交数据
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()

			return redirect('learning_logs:topics')
	'''显示空表单或指出单据无效'''
	context = {'form':form}
	return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
	'''在特定主题中添加内容'''
	topic = Topic.objects.get(id=topic_id)
	if request.method != "POST":
		#post 未提交数据,展示空表单呗
		form = EntryForm()
	else:
		#等于post提交数据
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learning_logs:topic',topic_id=topic_id)
	'''显示空表单或指出单据无效'''
	context = {'form':form,'topic':topic}
	# context = {'topic':topic,'form':form,'topic_id':topic_id}
	return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
	'''既有内容，又能添加内容'''
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.owner:
		raise Http404	

	if request.method != 'POST':
		#初次请求，使用当前条目作为填充表格
		form = EntryForm(instance=entry)
	else:
		#post 提交的数据:对数据进行处理
		form=EntryForm(instance=entry,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic',topic_id=topic.id)

	context={'entry':entry,'topic':topic,'form':form}
	return  render(request,'learning_logs/edit_entry.html',context)
			