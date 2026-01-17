Jekyll::Hooks.register :site, :post_read do |site|
  puts "HOOK: post_read"
end
Jekyll::Hooks.register :site, :pre_render do |site|
  puts "HOOK: pre_render"
end
