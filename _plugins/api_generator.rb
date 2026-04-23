require 'json'
require 'fileutils'

Jekyll::Hooks.register :site, :post_write do |site|
  puts "=== Generating API JSON files ==="
  
  # Helper to generate paginated JSON
  def generate_api_json(site, base_name, data, per_page)
    return unless data && data.is_a?(Array) && !data.empty?
    
    api_dir = File.join(site.dest, 'api', base_name)
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
      puts "  ✓ #{file_path}"
    end
  end
  
  # Generate Blogs API
  docs = site.pages.select { |p| p.data['layout'] == 'post' && (p.url.include?('/blogs/') || p.path.include?('blogs/')) }
  docs.reject! { |p| p.data['tags'] && (p.data['tags'].include?('Patent') || p.data['tags'].include?('Travelling') || p.data['tags'].include?('Moment')) }
  docs.reject! { |p| p.data['title'] && p.data['title'].include?('Moment') }
  docs = docs.sort { |a, b| (b.data['date'] || Time.now) <=> (a.data['date'] || Time.now) }
  
  blog_data = docs.map do |p|
    plain_text = p.content.to_s.gsub(/<[^>]+>/, '').gsub(/\[.*?\]\(.*?\)/, '').strip
    excerpt = p.data['subtitle'] || p.data['description'] || plain_text[0..200]
    {
      'title' => p.data['title'],
      'url' => p.data['permalink'] || p.url,
      'date' => p.data['date'] ? p.data['date'].to_s : '',
      'tags' => p.data['tags'] || [],
      'excerpt' => excerpt
    }
  end
  
  generate_api_json(site, 'blogs', blog_data, 20)
  
  # Generate Movies API
  if site.data['movies']
    if site.data['movies'].is_a?(Array)
      movies_data = site.data['movies']
      # Sort by pubdate/date descending
      movies_data = movies_data.sort_by { |m| 
        date = m['pubdate'] || m['date'] || '0000-00-00'
        parts = date.to_s.split('-')
        parts[0] = parts[0].to_s.rjust(4, '0')
        parts[1] = parts[1].to_s.rjust(2, '0') if parts[1]
        parts[2] = parts[2].to_s.rjust(2, '0') if parts[2]
        parts.join('-')
      }.reverse
      generate_api_json(site, 'movies', movies_data, 24)
    elsif site.data['movies'].is_a?(Hash)
      site.data['movies'].each do |key, movies|
        next unless movies.is_a?(Array)
        # Sort each sub-category
        sorted_movies = movies.sort_by { |m| 
          date = m['pubdate'] || m['date'] || '0000-00-00'
          parts = date.to_s.split('-')
          parts[0] = parts[0].to_s.rjust(4, '0')
          parts[1] = parts[1].to_s.rjust(2, '0') if parts[1]
          parts[2] = parts[2].to_s.rjust(2, '0') if parts[2]
          parts.join('-')
        }.reverse
        path = key == 'all' ? 'movies' : "movies/#{key}"
        generate_api_json(site, path, sorted_movies, 24)
      end
    end
  end
  
  # Generate Books API
  if site.data['books']
    books_data = site.data['books'].is_a?(Array) ? site.data['books'] : site.data['books']['all']
    if books_data
      # Sort by publish_date descending, using read_date as fallback
      books_data = books_data.sort_by { |b| 
        date = b['publish_date'] || b['read_date'] || '0000-00-00'
        parts = date.to_s.split('-')
        parts[0] = parts[0].to_s.rjust(4, '0')
        parts[1] = parts[1].to_s.rjust(2, '0') if parts[1]
        parts[2] = parts[2].to_s.rjust(2, '0') if parts[2]
        parts.join('-')
      }.reverse
      generate_api_json(site, 'books', books_data, 24)
    end
  end
  
  # Generate Games API
  if site.data['games']
    games_data = site.data['games'].is_a?(Array) ? site.data['games'] : site.data['games']['all']
    if games_data
      # Sort by release_date/date descending
      sorted_games = games_data.sort_by { |g| 
        date = g['release_date'] || g['date'] || '0000-00-00'
        parts = date.to_s.split('-')
        parts[0] = parts[0].to_s.rjust(4, '0')
        parts[1] = parts[1].to_s.rjust(2, '0') if parts[1]
        parts[2] = parts[2].to_s.rjust(2, '0') if parts[2]
        parts.join('-')
      }.reverse
      generate_api_json(site, 'games', sorted_games, 24)
    end
  end
  
  # Generate Douban API
  if site.data['douban']
    site.data['douban'].each do |year, statuses|
      next unless statuses.is_a?(Array)
      generate_api_json(site, "douban/#{year}", statuses, 30)
    end
  end
  
  puts "=== API JSON generation complete ==="
end
