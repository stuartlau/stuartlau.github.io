require 'json'
require 'fileutils'

puts "Testing API generation..."

# Create API directory
api_dir = File.join('_site', 'api', 'test')
FileUtils.mkdir_p(api_dir)
puts "Created directory: #{api_dir}"

# Write a test JSON file
test_data = {
  'page' => 1,
  'total_pages' => 1,
  'data' => ['test1', 'test2']
}

file_path = File.join(api_dir, 'page-1.json')
File.write(file_path, JSON.pretty_generate(test_data))
puts "Written file: #{file_path}"
puts "File exists: #{File.exist?(file_path)}"
