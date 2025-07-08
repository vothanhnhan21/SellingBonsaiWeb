from django.shortcuts import render,redirect, get_object_or_404
from .models import Plant, UserContact,CartItem,Invoice,InvoiceItem
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View 
from django.contrib.auth.models import User
from .forms import RegisterForm,rePasswordForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.templatetags.static import static
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            user = User.objects.create_user(password=password, username = username, email=email)
            
            phone = form.cleaned_data.get('phone')  
            address = form.cleaned_data.get('address')  

            user_contact = UserContact.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = RegisterForm()
        
    return render(request, 'signup.html',{'form': form})
def login_view(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"
    return render(request, 'signin.html', {'error_message':error_message})
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('home')
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get(self,request):
        return render(request, 'protected.html')
def index(request):
    products = Plant.objects.all()# lấy tất cả sản phẩm
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}#tạo nơi chứa sản phẩm cho giỏ hàng
    if request.user.is_authenticated:#kiểm tra xem người dùng có đăng nhập chưa
        cartItems = CartItem.objects.filter(user = request.user)
        #lấy các sản phẩm tương ứng với user
    return render(request,'index.html',{'page_obj':page_obj,'cart_items': cartItems})

def introduction(request):
    cartItems = {}
    if request.user.is_authenticated:
        cartItems = CartItem.objects.filter(user = request.user)
    return render(request,'introduction.html',{'cart_items': cartItems})

def news(request):
    cartItems = {}
    if request.user.is_authenticated:
        cartItems = CartItem.objects.filter(user = request.user)
    return render(request,'news.html',{'cart_items': cartItems})

def connection(request):
    cartItems = {}
    if request.user.is_authenticated:
        cartItems = CartItem.objects.filter(user = request.user)
    return render(request,'connection.html',{'cart_items': cartItems})

def policy(request):
    cartItems = {}
    if request.user.is_authenticated:
        cartItems = CartItem.objects.filter(user = request.user)
    return render(request,'policy.html',{'cart_items': cartItems})
@login_required # yêu cầu người dùng cần đăng nhập để xem được trang
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user) # lấy sản phẩm ứng với user tương ứng 
    return render(request, 'cart.html', {'cart_items': cart_items})
@login_required
def cart_mini_update(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        try:
            cart_items = CartItem.objects.filter(user=request.user) # lấy danh sách sản phẩm mới tương ứng người dùng 
            product_list = [] # tạo nơi chứa sản phẩm 
            for item in cart_items: # dùng for lấy những thông tin cần thiết của từng sản phẩm 
                item_data = {
                    'id': item.id,
                    'name': item.product.plant_name,
                    'price': item.product.price,
                    'image':item.product.image,
                    'quantity': item.quantity,
                }
                product_list.append(item_data)
            # trả về dữ liệu 
            return JsonResponse({ 
                'status': 'success',
                'cartProducts': product_list,
            })

        except CartItem.DoesNotExist: # trả về lỗi khi model không hoạt động đúng 
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy sản phẩm trong giỏ hàng!'})
@login_required
def add(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        item_id = request.GET.get('item_id')
        try:
            item = Plant.objects.get(id=item_id) # lấy sản phẩm tương ứng 
            
            return JsonResponse({
                'status': 'success',
                'product': {
                    'id': item_id, #id sản phẩm
                    'name': item.plant_name, # tên sản phẩm
                    'price': item.price, #giá sản phẩm
                    'image': item.image,  # tên ảnh 
                }
            })

        except Plant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy sản phẩm trong giỏ hàng!'})
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        item_id = request.POST.get('item_id') # lấy id sản phẩm
        quantity = int(request.POST.get('quantity',1)) # số lượng sản phẩm
        try:
            plant = Plant.objects.get(id=item_id) # lấy dữ liệu sản phẩm tương ứng

            # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
            cart_item = CartItem.objects.filter(product=plant, user=request.user).first()  # Lấy cart item của user hiện tại
            if cart_item: # nếu sản phẩm đã có trong giỏ hàng 
                cart_item.quantity += quantity # tăng số lượng sản phẩm
                cart_item.save()
            else: # nếu không
                cartItem = CartItem.objects.create(product=plant, quantity=quantity,user = request.user) # tạo một hàng mới tương ứng
                cartItem.save()
            message = 'Sản phẩm đã được thêm thành công!'
            return JsonResponse({
                'status': 'success',
                'message': message
            })

        except Plant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy sản phẩm trong giỏ hàng!'})
def update_cart_item_quantity(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id') 
        new_quantity = int(request.POST.get('quantity'))

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user) # lấy sản phẩm tương ứng trong giỏ hàng của người dùng
            
            # Kiểm tra xem số lượng có hợp lệ không
            if new_quantity < 1:
                return JsonResponse({'status': 'error', 'message': 'Số lượng phải lớn hơn hoặc bằng 1!'})

            # Cập nhật số lượng trong giỏ hàng
            cart_item.quantity = new_quantity 
            cart_item.save()

            # Tính lại tổng giá trị giỏ hàng

            return JsonResponse({
                'status': 'success',
                'message': 'Số lượng đã được cập nhật!'
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy sản phẩm trong giỏ hàng!'})
def delete_cart_item(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id') # lấy id sản phẩm trong giỏ hàng 

        try:
            # Lấy CartItem từ cơ sở dữ liệu tương ứng với id 
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)

            # Xóa sản phẩm trong cơ sở dữ liệu của giỏ hàng 
            cart_item.delete()
            
            # Trả lại phản hồi JSON
            return JsonResponse({
                'status': 'success',
                'message': 'Sản phẩm đã được xóa khỏi giỏ hàng!'
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Đã có lỗi xảy ra!'})

    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ!'})
def delete_all(request):
    cart_items = CartItem.objects.filter(user=request.user) # lấy sản phẩm tương ứng với user 
    cart_items.delete() # xóa toàn bộ sản phẩm 
    return redirect('cart') # điều hướng về lại trang 
def payment(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity',1))
        try:
            plant = Plant.objects.get(id=item_id)
            total_amount = plant.price * quantity
            invoice = Invoice.objects.create(user = request.user, total_amount = total_amount,status='pending')
            invoiceItem = InvoiceItem.objects.create(
            invoice=invoice,
            product=plant,
            quantity=quantity,
            price_at_time_of_purchase=plant.price
        )
            return JsonResponse({
                'status': 'success'
            })

        except Plant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy sản phẩm trong giỏ hàng!'})
def payment_page(request):
    
    cart_items_data = request.session.get('cart_items_data')  # Lấy dữ liệu giỏ hàng từ session
    user_address = UserContact.objects.get(user=request.user)
    if not isinstance(cart_items_data, list):
        total = cart_items_data['price'] * cart_items_data['quantity']
        if total > 0:
            return render(request, 'payment.html', {'product': cart_items_data,'total': total,"user_address":user_address})
    total = 0
    for i in cart_items_data:
        price = i.get('product__price', 0)
        quantity = i.get('quantity', 0)
        
        # Tính tổng tiền
        total += price * quantity
    if cart_items_data:
        return render(request, 'payment.html', {'cartItems': cart_items_data,'total': total,"user_address":user_address})
def payment_list(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        item_ids = request.POST.get('list_id')
        item_ids_list = [int(id) for id in item_ids.split(',')]
        cartItems = []
        try:
            if len(item_ids_list) == 1:
                product = Plant.objects.get(id = item_ids)
                product_result = {
                    'id': product.id,
                    'plant_name': product.plant_name,
                    'quantity': 1,
                    'price': product.price,
                    'image': product.image
                }
                request.session['cart_items_data'] = product_result  # Lưu dữ liệu vào session
                return JsonResponse({'status': 'success', 'next_url': '/payment_page/'})
            else:
                print(item_ids,'item_ids_list')
                for i in item_ids_list:
                    print(i)
                    cartItem = CartItem.objects.filter(product_id  = i,user = request.user).select_related('product').values('id','product_id','quantity','user_id','product__plant_name','product__price','product__image')
                    cartItems.extend(cartItem)
                
                request.session['cart_items_data'] = cartItems  # Lưu dữ liệu vào session
                return JsonResponse({'status': 'success', 'next_url': '/payment_page/'})
        except Plant.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy sản phẩm trong giỏ hàng!'})
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ!'})
def payment_submit(request):
    cart_items_data = request.session.get('cart_items_data')  # Lấy dữ liệu giỏ hàng từ session
    if not isinstance(cart_items_data,list):
        total = cart_items_data['price']*cart_items_data['quantity']
        invoice = Invoice.objects.create(user = request.user, total_amount = total,status='pending')
        invoiceItem = InvoiceItem.objects.create(
            invoice=invoice,
            product=Plant.objects.get(id = cart_items_data['id']),
            quantity=cart_items_data['quantity'],
            price_at_time_of_purchase=cart_items_data['price']
        )
        success = True  # Điều kiện thành công
    
        if success:
            # Gửi thông báo thành công
            messages.success(request, "Đơn hàng của bạn đã được tạo thành công!.")
        return redirect('home')
    total = 0
    for i in cart_items_data:
        price = i.get('product__price', 0)
        quantity = i.get('quantity', 0)
        
        # Tính tổng tiền
        total += price * quantity
    invoice = Invoice.objects.create(user = request.user, total_amount = total,status='pending')
    for i in cart_items_data:
        invoiceItem = InvoiceItem.objects.create(
            invoice=invoice,
            product=Plant.objects.get(id = i.get('product_id')),
            quantity=i.get('quantity'),
            price_at_time_of_purchase=i.get('product__price')
        )
        cart_item = CartItem.objects.get(id=i.get('id'), user=request.user)

        # Xóa sản phẩm khỏi giỏ hàng
        cart_item.delete()
    success = True
    messages.success(request, "Thanh toán thành công! Đơn của bạn đã được tạo.")
    return redirect('home')
#DMSP
def CTS(request):
    products = Plant.objects.filter(plant_type='CTS')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'DMSP/CTS.html',{'page_obj':page_obj,'cart_items': cartItems})
def CTN(request):
    products = Plant.objects.filter(plant_type='CTN')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'DMSP/CTN.html',{'page_obj':page_obj,'cart_items': cartItems})

def CSD(request):
    products = Plant.objects.filter(plant_type='CSD')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'DMSP/CSD.html',{'page_obj':page_obj,'cart_items': cartItems})

def CPT(request):
    products = Plant.objects.filter(plant_type='CPT')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'DMSP/CPT.html',{'page_obj':page_obj,'cart_items': cartItems})
def CNN(request):
    products = Plant.objects.filter(plant_type='CNN')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'DMSP/CNN.html',{'page_obj':page_obj,'cart_items': cartItems})
def CDB(request):
    products = Plant.objects.filter(plant_type='CDB')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'DMSP/CDB.html',{'page_obj':page_obj,'cart_items': cartItems})
def CCT(request):
    products = Plant.objects.filter(plant_type='CCT')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'DMSP/CCT.html',{'page_obj':page_obj,'cart_items': cartItems})

#CARE
def careCTS(request):
    products = Plant.objects.filter(plant_type='CCT')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'care/careCTS.html',{'page_obj':page_obj,'cart_items': cartItems})
def careCVP(request):
    products = Plant.objects.filter(plant_type='CCT')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'care/careCVP.html',{'page_obj':page_obj,'cart_items': cartItems})
def careSD(request):
    products = Plant.objects.filter(plant_type='CCT')
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        print(1)
        cartItems = CartItem.objects.filter(user = request.user)
        print(request.user.username)
    return render(request,'care/careSD.html',{'page_obj':page_obj,'cart_items': cartItems})

#find 
def find_page(request):
    query = request.POST.get('input-find', '').lower()  # lấy dữ liệu từ input search
    products = Plant.objects.filter(plant_name__icontains=query) # _icontains cho phép tìm kiếm các kết quả chứa hoặc khớp với dữ liệu tìm kiếm
    if products.exists() == False:
        products = Plant.objects.all()
        messages.success(request, "Sản phẩm sẽ có trong tương lai, chúng tôi có các sản phẩm tương tự!.")
    paginator = Paginator(products, 6)  # Mỗi trang sẽ có 6 sản phẩm
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy trang hiện tại
    cartItems = {}
    if request.user.is_authenticated:
        cartItems = CartItem.objects.filter(user = request.user)
    return render(request,'find_page.html',{'page_obj':page_obj,'cart_items': cartItems})
    # has_product trả về kết quả true hoặc false về việc tìm kiếm có kết quả hay không
@login_required
def change_password(request):
    if request.method == 'POST':
        form = rePasswordForm(request.POST,instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            return render(request, 'change_password.html', {'form': form})
    else:
        form = rePasswordForm(instance=request.user)
        
    return render(request, 'change_password.html',{'form': form})