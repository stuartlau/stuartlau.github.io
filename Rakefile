require 'json'
require 'fileutils'

desc "Generate API JSON files"
task :generate_api do
  puts "=== Generating API JSON files ==="
  
  # Helper to generate paginated JSON
  def generate_api_json(base_name, data, per_page)
    return unless data && data.is_a?(Array) && !data.empty?
    
    api_dir = File.join('_site', 'api', base_name)
    FileUtils.mkdir_p(api_dir)
    
    total_pages = (data.length.to_f / per_page).ceil
    puts "  Creating #{total_pages} pages for #{base_name} (#{data.length} items)"
    
    (1..total_pages).each do |page|
      start_index = (page - 1) * per_page
      end_index = [start_index + per_page, data.length].min - 1
      page_items = data[start_index..end_index]
      
      json_data = {
        'page' => page,
        'total_pages' => total_pages,
        'total_count' => data.length,
        'data' => page_items
      }
      
      file_path = File.join(api_dir, "page-#{page}.json")
      File.write(file_path, JSON.pretty_generate(json_data))
      puts "  ✓ Created #{file_path}"
    end
  end
  
  # Load and generate Movies API
  if File.exist?('_data/movies/all.json')
    movies_data = JSON.parse(File.read('_data/movies/all.json'))
    generate_api_json('movies', movies_data, 24)
  end
  
  # Load and generate Books API
  if File.exist?('_data/books/all.json')
    books_data = JSON.parse(File.read('_data/books/all.json'))
    generate_api_json('books', books_data, 24)
  end
  
  # Load and generate Games API
  if File.exist?('_data/games/all.json')
    games_data = JSON.parse(File.read('_data/games/all.json'))
    generate_api_json('games', games_data, 24)
  end
  
  # Load and generate Douban API for each year
  Dir.glob('_data/douban/*.json').each do |file|
    year = File.basename(file, '.json')
    douban_data = JSON.parse(File.read(file))
    generate_api_json("douban/#{year}", douban_data, 30)
  end
  
  puts "=== API JSON generation complete ==="
end

desc "Build site and generate API"
task :build => [:generate_api] do
  sh "bundle exec jekyll build"
  Rake::Task[:generate_api].execute
end
