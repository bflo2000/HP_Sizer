#!/usr/bin/python
import csv, sys, math, operator, re, os
from utils import photo_sizer

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

newCsv = []
newFile = open('photo_variations.csv', 'wb') #wb for windows, else you'll see newlines added to csv

# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

# write amazon's headers
header_row1 = ('TemplateType=home', 'Version=2014.1119')

header_row2 = ('Item Type Keyword', 'Product Name', 'Product Description', 'Product Type', 
	'Brand Name', 'Manufacturer', 'Manufacturer Part Number', 'SKU', 'Parent SKU', 'Parentage', 'Relationship Type', 
	'Variation Theme', 'Size', 'Update Delete', 'Standard Price', 'Quantity', 'Product Tax Code', 'Package Quantity', 'Shipping Weight', 'Website Shipping Weight Unit Of Measure', 
	'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5','Main Image URL', 'Shipping-Template', 'Search Terms')

header_row3 = ('item_type', 'item_name', 'product_description', 'feed_product_type', 
	'brand_name', 'manufacturer', 'part_number', 'item_sku', 'parent_sku','parent_child', 'relationship_type', 
	'variation_theme', 'size_name', 'update_delete', 'standard_price', 'Quantity', 'product_tax_code', 'item_package_quantity', 'website_shipping_weight', 'website_shipping_weight_unit_of_measure',
	'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5','main_image_url', 'merchant_shipping_group_name', 'generic_keywords')

# initialize csv writer
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)
writer.writerow(header_row2)
writer.writerow(header_row3)

# write the dictionary, do some calculations on the way
for item in newCsv:

	try:
		sku = item['Sku']
	except:
		try:
			sku = item['item_sku']
		except:
			try:
				sku = item['SKU']
			except:
				sku = item['Title']
	try:
		image_width = float(item['ImageWidth'])
	except:
		print "Warning: Image Width not formatted in SKU: " + sku
		continue
	try:
		image_height = float(item['ImageHeight'])
	except:
		print "Warning: Image Height not formatted in SKU: " + sku
		continue

	item_sizes = photo_sizer(image_height, image_width, sku)

# ------------------------------------------------------------------------------------ end filter
	try:
		image_name = item['ImageName']
	except:
		try:
			image_name = item['Image Name']
		except:
			try:
				image_name = item['Image_Name']
			except:
				print "Please format the ImageName field: ImageName. Image Name, or Image_Name."
				exit()

	bullet_point1 = "Giclee Photo Print on High Quality Archival Luster Photo Paper"
	bullet_point2 = "Professionally Printed Vintage Fine Art Photographic Reproduction"
	bullet_point3 = "Perfect for the home or office - makes a great gift"
	bullet_point4 = "100% Satisfaction Guaranteed"
	try:
		bullet_point5 = item['Title']
	except:
		bullet_point5 = ""

	try:
		keywords = item['Keywords']
	except:
		try:
			keywords = item['Generic Keywords']
		except:
			print "Warning: no Keyword field defined."

	brand_name = 'Historic Pictoric'
	manufacturer = 'Historic Pictoric'
	main_image_url = "www.historicpictoric.com/media/AMZWebImg/SoldProductsUpdate/" + image_name
	feed_product_type = "art"
	item_type = "Photograph"
	
	try:
		item_name = item['Title']
	except:
		try:
			item_name = item['Item Name']
		except:
			print "Warning: No Title or Item Name field defined for Sku:" + sku
	
	try:
		item_sizename = item['Size Name']
	except:
		try:
			item_sizename = item['SizeName']
		except:
			try:
				item_sizename = item['Size_Name']
			except:
				print "Please format the SizeName field of your input: SizeName, Size Name, or Size_Name."

	parent_sku = sku + "P"
	product_description = "<p>" + item_name + "</p>"
	part_number =  parent_sku 
	parent_child = "parent" # leave blank for children
	item_sku = parent_sku
	relationship_type = ""
	variation_theme = "size"
	size_name = ""
	update_delete = ""
	standard_price = ""
	quantity = ""
	product_tax_code = ""
	item_package_quantity = ""
	website_shipping_weight = ""
	website_shipping_weight_unit_of_measure = ""
	merchant_shipping_group_name = ""
	size_name_actual = ""
	
	write_tuple = (item_type, item_name, product_description, feed_product_type, brand_name, manufacturer,
		part_number, item_sku, "", parent_child, relationship_type, variation_theme, size_name,
		update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
		website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
		bullet_point5, main_image_url, merchant_shipping_group_name, keywords)

	writer.writerow(write_tuple)

	for size in item_sizes:
		product_description = "<p>" + item_name + "</p>"
		item_sku = sku

		number1 = str(re.findall(r'\d+', size['SizeName'])[0])
		number2 = str(re.findall(r'\d+', size['SizeName'])[1])

		# format the size names so that they're all alike
		formatted_sizename = re.sub('[ xin]', '', size['SizeName2'])
		formatted_comparison = re.sub('[ xin]', '', item_sizename)
		part_number_str = re.sub('[ xin]', '', size['SizeName'])
		parent_child = ""
		part_number =  sku + "_" + part_number_str
		item_sku = sku + "_" + part_number_str
		size_name = size['SizeName']
		update_delete = ""
		relationship_type = "variation"
		variation_theme = "size"
		standard_price = size['Price']
		quantity = "10"
		product_tax_code = 'a_gen_tax'
		item_package_quantity = "1"
		website_shipping_weight = "1"
		website_shipping_weight_unit_of_measure = "lbs"
		bullet_point5 = item_name
		merchant_shipping_group_name = "Free_Economy_Shipping_16x20"

		try:
			image_name = item['ImageName']
		except:
			try:
				image_name = item['Image Name']
			except:
				try:
					image_name = item['Image_Name']
				except:
					print "Please format the ImageName field: ImageName. Image Name, or Image_Name."
					exit()

		write_tuple = (item_type, item_name, product_description, feed_product_type, brand_name, manufacturer,
			part_number, item_sku, parent_sku, parent_child, relationship_type, variation_theme, size_name,
			update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
			website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
			bullet_point5, main_image_url, merchant_shipping_group_name, keywords)

		writer.writerow(write_tuple)

newFile.close()

