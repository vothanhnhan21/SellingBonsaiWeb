
$(document).ready(function() {
    
    function getCsrfToken() {
        var name = 'csrftoken';
        var value = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return value ? value.pop() : '';
    };

    // Thêm CSRF token vào header của tất cả các yêu cầu AJAX
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': getCsrfToken()
        }
    });

    $('.add').on('click',function() { // lắng nghe sự kiện người dùng click icon giỏ hàng trên mỗi sản phẩm
        
        var ItemId = $(this).data('cart-item-id'); // lấy id của sản phẩm tương ứng
        // Gửi yêu cầu AJAX để cập nhật số lượng
        $.ajax({
            url: addURL, 
            type: 'GET',
            data: {
                'item_id': ItemId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) { // xử lý dữ liệu trả về thành công
    
                if (response.status === 'success') { // hiển thị display với sản phẩm tương ứng mà người dùng muốn thêm 
                    var imageUrl = "/static/images/" + response.product.image; // tạo đường link tới ảnh của sản phẩm
                    var price = ' '+response.product.price + ' VNĐ' // tạo hiển thị giá sản phẩm 
                    $('#product-cart-img').attr('src', imageUrl); // hiển thị ảnh 
                    $('#cart-price-content').html(price); // hiển thị giá sản phẩm
                    $('#product-cart-name').html(response.product.name); // hiển thị tên sản phẩm
                    $('.add_complete').attr('value', response.product.id); // truyền id sản phẩm vào nút thêm vào giỏ hàng 
                    $('.add-to-cart-display').removeClass('hidden');

                } else {
                    alert(response.message); // hiển thị thông báo lỗi 
                }
            },
            error: function() { // hiển thị thông báo lỗi 
                alert('Có lỗi xảy ra. Vui lòng thử lại!');
            }
        });
    });
    $('.add_complete').on('click',function() {
        var ItemId = $(this).attr('value'); // lấy id sản phẩm
        var quantity = $('cart-quantity').value; // số lượng của sản phẩm 
        // gửi yêu cầu 
        $.ajax({
            url: addURL,
            type: 'POST',
            data: {
                'item_id': ItemId,
                'quantity': quantity,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('.add-to-cart-display').addClass('hidden'); // ẩn lớp thêm sản phẩm 
                    update_cart_item(); // gọi hàm cập nhập sản phẩm trong giỏ hàng          
                    var message = response.message; // lấy thông báo từ phản hồi

                    // Tạo phần tử li mới cho thông báo
                    const li = document.createElement('li');
                    li.classList.add('alert', 'alert-info', 'message-item');
                    li.textContent = message;

                    // Thêm thông báo vào container
                    const container = document.querySelector('.notification-container ul');
                    container.appendChild(li);

                    // Hiệu ứng hiển thị thông báo
                    setTimeout(function() {
                        li.style.transition = "opacity 1s";
                        li.style.opacity = '0'; // Fade out the message
                        setTimeout(function() {
                            li.style.display = 'none'; // Ẩn thông báo sau khi fade
                        }, 1000); // Sau 1 giây (thời gian fade)
                    }, 2000);  // Hiển thị thông báo sau 2 giây
                }
                else {
                    alert(response.message); // thông báo lỗi 
                }
            },
            error: function() {
                alert('Có lỗi xảy ra. Vui lòng thử lại!');
            }
        });
    });
    $('.payment-submit').on('click',function() {
        var ItemId = $(this).attr('value');
        var quantity = $('payment-quantity').value;
        $.ajax({
            url: payment,
            type: 'POST',
            data: {
                'item_id': ItemId,
                'quantity': quantity,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                console.log(response);
                if (response.status === 'success') {
                    alert('Đơn hàng được đặt thành công');
                    $('.payment-display').addClass('hidden');

                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('Có lỗi xảy ra. Vui lòng thử lại!');
            }
        });
    });
    $('#payment-quantity').on(function(){
        var quantity = $(this).val();
        var priceTex = $('#payment-price-content').text();
        var price = priceTex.replace('VNĐ', '').trim();
        price = parseFloat(price);
        $('#total').html(price+'VNĐ');
    });
    $('#payment-quantity').on('change',function(){
        var quantity = $(this).val();
        var priceTex = $('#payment-price-content').text();
        var price = priceTex.replace('VNĐ', '').trim();
        price = parseFloat(price);
        var total = price * quantity;
        $('#total').html(total+'VNĐ');
    });
    $('.add-to-cart-cancel').on('click',function() {
        $('.add-to-cart-display').addClass('hidden');
    });
    $('.purchase').click(function() {
        var ItemId = $(this).data('cart-item-id');
        console.log(paymentListUrl);
        $.ajax({
                url: paymentListUrl,
                type: 'POST',
                data: {
                    'list_id': ItemId,
                    'csrfmiddlewaretoken': csrfToken 
                },
                success: function(response) {
                if (response.status === 'success') {
                    console.log('success');
                    window.location.href = response.next_url;
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('Có lỗi xảy ra. Vui lòng thử lại!');
            }
            });
    });
    function update_cart_item(){
        $.ajax({
            url: cartMiniUpdate,
            type: 'GET',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('.cart-content').empty();
                    var cart = response.cartProducts; 
                    // Mảng chứa các phần tử HTML cho giỏ hàng mini
                    var new_content = [];

                    for(var item of cart) {
                            console.log(item.image);
                            var html = '<div class="product-cart">' +
                                '<img src="/static/images/'+item.image+'" style="width: 80px;" alt="Sản phẩm">' +
                                '<h3>' + item.name + '</h3>' +
                                '<span class="price">' + item.price + ' VNĐ</span>' +
                                '<span class="quantity">' + item.quantity + ' Cây</span>' +
                                '</div>';
                    
                            new_content.push(html);
                        };
                    $('.cart-content').html(new_content.join(''));

                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('Có lỗi xảy ra. Vui lòng thử lại!');
            }
        });
    };
});

var cart = document.getElementById('cart-icon'); // Chọn phần tử cart-icon đúng cách
cart.addEventListener('mouseenter', function() {
    var triangleCart = document.querySelector('.triangle-cart'); // Chọn phần tử triangle-cart
    var cart_mini = document.querySelector('.cart'); // Chọn phần tử cart

    // Thêm lớp 'represent' cho các phần tử
    triangleCart.classList.add('represent');
    cart_mini.classList.add('represent');
});
var cartOut = document.querySelector('.shopping-cart'); 
cartOut.addEventListener('mouseleave', function() {
    var triangleCart = document.querySelector('.triangle-cart'); // Chọn phần tử triangle-cart
    var cart_mini = document.querySelector('.cart'); // Chọn phần tử cart

    triangleCart.classList.remove('represent');
    cart_mini.classList.remove('represent');
});