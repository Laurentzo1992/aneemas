/*! Select2 4.1.0-rc.0 | https://github.com/select2/select2/blob/master/LICENSE.md */
var dalLoadLanguage=function(n){var t;(t=n&&n.fn&&n.fn.select2&&n.fn.select2.amd?n.fn.select2.amd:t).define("select2/i18n/vi",[],function(){return{inputTooLong:function(n){return"Vui lòng xóa bớt "+(n.input.length-n.maximum)+" ký tự"},inputTooShort:function(n){return"Vui lòng nhập thêm từ "+(n.minimum-n.input.length)+" ký tự trở lên"},loadingMore:function(){return"Đang lấy thêm kết quả…"},maximumSelected:function(n){return"Chỉ có thể chọn được "+n.maximum+" lựa chọn"},noResults:function(){return"Không tìm thấy kết quả"},searching:function(){return"Đang tìm…"},removeAllItems:function(){return"Xóa tất cả các mục"}}}),t.define,t.require},event=new CustomEvent("dal-language-loaded",{lang:"vi"});document.dispatchEvent(event);