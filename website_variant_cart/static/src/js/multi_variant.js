/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('website_variant_cart.multi_variant', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var core = require('web.core');
    var utils = require('web.utils');
    var _t = core._t;

    $(document).ready(function() {

        function str_to_price(str_price) {
            var l10n = _t.database.parameters;
            str_price = str_price.replace(l10n.thousands_sep, '');
            str_price = str_price.replace(l10n.decimal_point, '.');
            return parseFloat(str_price)
        }

        function price_to_str(price) {
            var l10n = _t.database.parameters;
            var precision = 2;
            if ($(".decimal_precision").length) {
                precision = parseInt($(".decimal_precision").last().data('precision'));
                if (!precision) { precision = 0; } //todo: remove me in master/saas-17
            }
            var formatted = _.str.sprintf('%.' + precision + 'f', price).split('.');
            formatted[0] = utils.insert_thousand_seps(formatted[0]);
            return formatted.join(l10n.decimal_point);
        }

        function update_total_price(){
            var total = 0.0;
            var $form = $('.p_variants').closest("form");
            var $total_price = $form.find('#var-total-price');
            $('.p_variants').each(function(){
                var $subtotal = $(this).find('#var-subtotal');
                var subtotal = str_to_price($subtotal.find('.oe_currency_value').html());
                total = total + subtotal;
            });
            $total_price.find('.oe_currency_value').html(price_to_str(total));
        }

        function getCustomVariantValues(container) {
          var variantCustomValues = [];
          container.find('.p_variants_cust_val').each(function (){
              var $variantCustomValueInput = $(this);
              if ($variantCustomValueInput.length !== 0){
                  variantCustomValues.push({
                      'custom_product_template_attribute_value_id': $variantCustomValueInput.data('attribute_value_id'),
                      'attribute_value_name': $variantCustomValueInput.data('attribute_value_name'),
                      'custom_value': $variantCustomValueInput.val(),
                  });
              }
          });
          return variantCustomValues;
        }

        $('.p_variants').find('input[type="text"][name="add_qty"]').on('change', function(ev)
        {
            var $p_variants = $(this).closest('.p_variants');
            var add_qty = parseInt($(this).val(),10);
            var $subtotal = $p_variants.find('#var-subtotal');
            var $var_price = $p_variants.find('#var-price');
            var product_id = parseInt($p_variants.find('input[type="hidden"][name="product_id"]').first().val(),10);
            if(add_qty > 0){
                ajax.jsonRpc("/vc/shop/get_unit_price", 'call', {'product_ids': product_id,'add_qty': add_qty})
                .then(function (data) {
                    var value = data[product_id];
                    $var_price.find('.oe_currency_value').html(price_to_str(value));
                    $subtotal.find('.oe_currency_value').html(price_to_str(value*add_qty));
                    update_total_price();
                });
            }
            else{
                $subtotal.find('.oe_currency_value').html(price_to_str(0));
                update_total_price();
            }
        });

        var publicWidget = require('web.public.widget');
        require('website_sale.website_sale');

        publicWidget.registry.WebsiteSale.include({
            _onClickAdd: function(ev){
                ev.preventDefault();
                var variant_list_status = $('#variants_list_view_status').data('variant_list_status');
                if(!variant_list_status){
                    return this._handleAdd($(ev.currentTarget).closest('form'));

                }
                var data = [];
                if (!$(ev.currentTarget).is(".disabled")) {
                    var variant_element = document.getElementById('p_variants');
                    if (variant_element != null) {
                        $('.p_variants').each(function(ev){
                            var dict = {};
                            var $this = $(this);
                            var product_id = parseInt($this.find('input[type="hidden"][name="product_id"]').first().val(),10);
                            var add_qty = parseInt($this.find('input[name="add_qty"]').first().val(),10);
                            var custom_value = getCustomVariantValues($this)
                            if(!isNaN(add_qty) && add_qty > 0){
                                dict["product_id"] = product_id;
                                dict["add_qty"] = add_qty;
                                dict['product_custom_attribute_values']= JSON.stringify(custom_value);
                                data.push(dict);
                            }
                        });
                        if(data.length == 0){
                            $('#multi-variant-error').show();
                            setTimeout(function() {
                                $('#multi-variant-error').hide();
                            },3000);
                        }
                        else{
                            ajax.jsonRpc("/shop/cart/update/multi/variant", 'call',
                            {
                                'data': data,
                            })
                            .then(function (result)
                            {
         	                    window.location.href = window.location.origin + result['redirect_url']
                                $(window).on('load',function() {});
                            });
                        }
                    }
                    else{
                        return this._handleAdd($(ev.currentTarget).closest('form'));
                    }
                }
            }

        });

    });
});
