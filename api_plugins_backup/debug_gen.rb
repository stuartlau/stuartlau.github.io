module StuartLau
  class DebugGenerator < Jekyll::Generator
    def generate(site)
      puts "DEBUG: Pages count: #{site.pages.size}"
      site.pages.each do |p|
        if p.url.include?('api/')
          puts "DEBUG: API Page: #{p.url} name: #{p.name} dest: #{p.destination(site.dest)}"
        end
      end
    end
  end
end
