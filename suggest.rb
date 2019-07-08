
# normal blocks: lower-case a-f, with aluminium: upper case
# empty field: .
# booster: 0-2
# chicken/pepper: 3
# sauce 4


class Board
	attr_accessor :board, :w, :h
	def initialize(board)
		@board = convert(board).split("\n").map{|e| ("."+e+".").split("")}
		@board.push(Array.new(@board[0].size,"."))
		@board.unshift(Array.new(@board[0].size,"."))
		@w = @board[0].size
		@h = @board.size
		@stack = []
	end

	def convert(board)
	  return board.tr("swmfkpSWMFKP", "abcdefABCDEF")
	end

	def push
		@stack.push(@board)
		@board = Array.new(@h){|y| Array.new(@w){|x| String.new(@board[y][x])}}
	end

	def pop
		@board = @stack.pop
	end

	def checkrows(tabu, mark,num)
		marked = false
		booster = []
		for y in 1...(@h-1)
			counter = 0
			what = "."
			for x in 1...(@w-1)
				if @board[y][x].downcase =~ /[a-h]/ && !tabu[y][x]
					if what==@board[y][x].downcase
						counter+=1
						if counter>=num
							counter.times{|i|
								mark[y][x-i]=true
							}
							marked = true
							if (num==4)
								booster.push([1,x-1,y])
							elsif num==5
								booster.pop
								booster.push([2,x-2,y])
							end
						end
					else
						what = @board[y][x].downcase
						counter = 1
					end
				else
					counter = 0
				end
			end
		end
		return marked, booster 
	end
	
	def checkcols(tabu, mark,num)
		marked = false
		booster = []
		for x in 1...(@w-1)
			counter = 0
			already = false
			maxboost = false
			what = "."
			for y in 1...(@h-1)
				if @board[y][x].downcase =~ /[a-h]/ && !tabu[y][x]
					if what==@board[y][x].downcase
						counter+=1
						already ||= mark[y][x]
						if counter>=num
							# puts "x,y = #{x},#{y}, counter=#{counter}, what=#{what}"
							counter.times{|i|
								mark[y-i][x]=true
							}
							marked = true
							if already && counter>=num && !maxboost
								maxboost = true
								booster.push([2,x,y])
							elsif !maxboost
								if (num==4)
									booster.push([1,x,y-1])
								elsif num==5
									booster.pop
									booster.push([2,x,y-2])
								end
							end
						end
					else
						what = @board[y][x].downcase
						maxboost = false
						counter = 1
						already = mark[y][x]
					end
				else
					counter = 0
					already = false
					maxboost = false
				end
			end
		end
		return marked, booster
	end

	def check(onlytruefalse=false, move=nil)
		mark = Array.new(@h){Array.new(@w,false)}
		marked = false
		booster = []  # [ [kind, x,y], ... ]
		if move!=nil
			move.push([move[0][0]+move[1][0],move[0][1]+move[1][1]])
		end
		# 2x2
		for y in 1...(@h-2)
			for x in 1...(@w-2)
				if @board[y][x].downcase =~ /[a-h]/ && !mark[y][x]
					if [[1,0],[0,1],[1,1]].all?{|d| @board[y+d[1]][x+d[0]].downcase==@board[y][x].downcase}
						[[0,0],[1,0],[0,1],[1,1]].each{|d|
							mark[y+d[1]][x+d[0]] = true
							if move!=nil
								[0,2].each{|i|
									if move[i][0]==x+d[0] && move[i][1]==y+d[1]
										booster.push([0,move[i][0], move[i][1]])
									end
								}
							end
						}
						if move==nil
								booster.push([0,x,y])
						end
						marked = true
						# puts self.to_s(mark)
						# puts "found 2x2 at #{x}=x, #{y}=y"
						return true if onlytruefalse
					end
				end
			end
		end
		mark2 = Array.new(@h){Array.new(@w,false)}
		mrkd,boost = checkrows(mark,mark2,3)
	  marked ||= mrkd	
		booster+=boost
		# puts self.to_s(mark2) if marked
		return true if marked && onlytruefalse
		mrkd,boost = checkcols(mark, mark2,3)
		marked||=mrkd
		booster += boost
		#puts self.to_s(mark2) if marked
		@h.times{|y| @w.times{|x| mark[y][x] = mark[y][x] || mark2[y][x]}}
		# puts self.to_s(mark) if marked
		return marked, mark, booster
	end

	def to_s(mark1=nil, makr2=nil)
		res = ""
		for y in 1...(@h-1)
			for x in 1...(@w-1)
				if (mark1!=nil && mark1[y][x])
					res += "\u001b[31m#{@board[y][x]} \u001b[0m"
				else
					res += @board[y][x]+" "
				end
			end
			res += "\n"
		end
		return res
	end	

	def alu?(x)
		return x=~/[A-H]/
	end

	def switchAlu(x)
		return x.upcase if x=~/[a-h]/
		return x.downcase
	end

	def execMove(m,debug=false)
		boosterCrush = false
		if m!=nil
			x,y = *m[0]
			dir = m[1]
			a,b = x+dir[0], y+dir[1]
			z = @board[y][x]
			c = @board[b][a]
		end
		points = 0

		booster = []
		puts "exec move=#{m.inspect}" if debug
		mark = Array.new(@h){Array.new(@w,false)}
		if m!=nil && z=~/[0-2]/ #Booster
			if c !~ /[0-2]/  # Das andere ist kein booster
				if z=="0" # Kartoffel
					[[-1,0],[0,0],[1,0],[0,1],[0,-1]].each{|d|
						bb = @board[b+d[1]][a+d[0]]
						if bb!="." && bb !~ /[34]/ # Chili/Poulet und Sauce gehen nicht weg
							mark[b+d[1]][a+d[0]] = true
							boosterCrush = true
						end
					}	
				elsif z=="1" # Spiess
					if dir[0]==0 # Vertikal
						for yy in 1...(@h-1)
							bb = @board[yy][x]
							if bb!="." && bb !~ /[34]/ # Chili/Poulet und Sauce gehen nicht weg
								mark[yy][x] = true
								boosterCrush = true
							end
						end
					else # Horizontal
						for xx in 1...(@w-1)
							bb = @board[y][xx]
							if bb!="." && bb !~ /[34]/ # Chili/Poulet und Sauce gehen nicht weg
								mark[y][xx] = true
								boosterCrush = true
							end
						end
					end

				else # Hamburger
					other = c.downcase
					for yy in 1...(@h-2)
						for xx in 1...(@w-2)
							if @board[yy][xx].downcase==other
								mark[yy][xx] = true
								boosterCrush = true
							end
						end
					end
					mark[y][x] = true
				end
			else # Doppelboost
				# Kartoffel zu Hamburger: 7x7 Feld weg
				# Hamburger zu Kartoffel: 2x horizontal und vertikal
				points += 3000 # Guestimate generously some points ;-)
			end
		else
			if m!=nil
				# swap items (respecting alu)
				@board[y][x], @board[b][a] = @board[b][a], @board[y][x]
				if alu?(@board[y][x])!=alu?(@board[b][a])
					# puts "ungleiche alu!"
					@board[y][x] = switchalu(@board[y][x])
					@board[b][a] = switchalu(@board[b][a])	
				end
			end
			marked, mark, booster = check()
			if debug
				puts "No more marked" unless marked
			end
			return 0 unless marked	
		end
		if debug
			puts "EXEC on "
			puts self.to_s(mark)
			puts "-------------------"
	  end
		# remove sauce
	    unless boosterCrush
			for yy in 1...(@h-1)
				for xx in 1...(@w-1)
					if @board[yy][xx]=="4" && !mark[yy][xx] &&
							[[1,0],[0,1],[0,-1],[-1,0]].any?{|d| mark[yy+d[1]][xx+d[0]]}
						@board[yy][xx] = ('a'.ord+rand(6)).chr
						points+=1000  # Removing Sauce is good!
					end
				end
			end
		end
		# remove marked
		for yy in 1...(@h-1)
			for xx in 1...(@w-1)
				if mark[yy][xx]
					if @board[yy][xx]=~/[A-H]/
						points+=1000  # Removing alu is good
					end
					@board[yy][xx] = " "
					points += 100
				end
			end
		end
		# Add boosters, if any
		booster.each{|b|
			@board[b[2]][b[1]] = b[0].to_s
		}
		if debug
			puts "EXPLODED"
			puts self.to_s()
			puts "-"*20
		end
		
		# Remove piment/poulet
		for xx in 1..(@w-1)
			yy = @h-2
			while yy>0 && @board[yy][xx]=~/[ .]/
				yy-=1
			end
			while yy>0 && @board[yy][xx]=='3'  # Piment/poulet
				@board[yy][xx] = ' '
				points+=2000  # Removing piment/poulet
				removed = true
				yy-=1
			end
		end

		
		# compact field and refill
		alu = Array.new(@h){|yy| Array.new(@w){|xx| @board[yy][xx]=~/[A-H]/}}
		for xx in 1..(@w-1)
			full = @h-2
			(@h-2).downto(1){|yy|
				if @board[yy][xx]==" "
					while (full>=1 && @board[full][xx] =~/[ .]/)
						full-=1
					end
					if (full<1)
						@board[yy][xx] = ('a'.ord+rand(6)).chr
					else
						@board[yy][xx] = @board[full][xx].downcase
						@board[full][xx] = " "
					end
					if alu[yy][xx]
						@boad[yy][xx].upcase!
					end
				else
					full-=1
				end
			}
		end
		if debug
			puts "FILLED "
			puts to_s
		end
		
		
		if (points>0)
			points += execMove(nil, debug)
		end

		return points
	end
	
	def moves
		res = []
		for y in 1...(@h-1)
			for x in 1...(@w-1)
				if @board[y][x]!="." # Check if sauce is moveable
					[[1,0],[0,1],[-1,0],[0,-1]].each.with_index{|d,i|
						a,b = x+d[0],y+d[1]
						if @board[b][a]!="."
							if @board[y][x]=~/[0-2]/
								unless @board[y][x]=="2" && @board[b][a]=="3"  # Cannot hamburgize piment/poulet
									res.push([[x,y],d])
								end
							elsif i<2 && @board[b][a].downcase =~ /[a-h]/
								self.push()
								mark = Array.new(@h){Array.new(@w,false)}
								# puts "\n\nVorher"
								# puts self.to_s
								mark[y][x] = true
								mark[b][a] = true
	
								@board[y][x], @board[b][a] = @board[b][a], @board[y][x]
								if alu?(@board[y][x])!=alu?(@board[b][a])
									# puts "ungleiche ALU!"
									@board[y][x] = switchAlu(@board[y][x])
									@board[b][a] = switchAlu(@board[b][a])	
								end
								# puts "Nacher: "
								# puts self.to_s(mark)
								c,m = check(false)
								if c
									# puts "Found:"
									# puts self.to_s(mark)
									res.push([[x,y],d])
								end
								self.pop()
							end
						end
					}	
				end	
			end
		end
		return res
	end

	def bestMove(iter=0)
		bestpoints = 0
		bestmove = nil
		n=7
		moves().each{|move|
			points = 0
			n.times{
				self.push()
				if iter==0	
					points += self.execMove(move)
				else
					p,m = self.bestMove(iter-1)
					points += p
				end
				self.pop()
			}
			if points>bestpoints
				bestpoints = points
				bestmove = move
			end
		}
		return bestpoints, bestmove
	end

	def compact
		return @board.map{|l| l[1..-2].join}[1..-2].join("\n")
	end

	def movemark(move)
		x,y = move[0][0], move[0][1]
		a,b = x+move[1][0], y+move[1][1]

		mark = Array.new(@h){Array.new(@w,false)}
		# puts "\n\nVorher"
		# puts self.to_s
		mark[y][x] = true
		mark[b][a] = true
		return mark

	end

end

if false
	b = Board.new("..abc..\n.edefd.\ncae0ece\nfacdbca\nfbfcedd\nafdfafb\ndddaceb\n.afdba.\n..cef..")
	puts b.to_s
	marked, mark, boost = b.check()
	puts "#{marked}, #{mark.inspect}, #{boost.inspect}"
	exit
end

# b = Board.new("..swm..\n.sfkpf.\nmkk0kmk\npfmfwms\np1pmkff\nspfpspw\nfwfsmkw\n.spfws.\n..mkp..")
b = Board.new("..fks..\nwkmpfkp\n4fsmk44\nwmkkmfk\n4pp4pkm\nmwpwmwm\nwskm4pp\n..mff..") # Level 107?

if ARGV.length > 0
  content = STDIN.read
  content = content.chomp
  b = Board.new(content)
end

total = 0
1.times{
	pts, move = b.bestMove(0)

	break if move==nil

	puts "Bestmove ist #{move.inspect} with #{pts/7}"

	puts b.to_s(b.movemark(move))
	puts "-"*20
	total += b.execMove(move, true)
	puts b.to_s
	puts "\nb = Board.new(#{b.compact.inspect})\n\n"
	puts "Point total = #{total}"
	puts "="*20
}

