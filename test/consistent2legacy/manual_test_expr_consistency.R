
## Manually Check Consistency
#
# Adapt to your system
library(readr)
# celseq2 <- read_csv("celseq2_demo.csv")
# expression_1M <- read_delim("expression_1M.tab",
#                             "\t", escape_double = FALSE,
#                             trim_ws = TRUE)

newexpr <- celseq2
oldexpr <- expression_1M[1:nrow(newexpr), ] ## tail several lines unwanted

## Whether rownames are consistent
rownames_newexpr <- unlist(c(newexpr[, 1]))
rownames_oldexpr <- unlist(c(oldexpr[, 1]))
table(rownames_newexpr == rownames_oldexpr)

## Make sure you are comparting the same cell
## as the cells names are not necessarily same
new_col_id <- 18
old_col_id <- 18
print(colnames(newexpr)[new_col_id])
print(colnames(oldexpr)[old_col_id])

## Test whether genes have different UMI counts for same cell
conflict <- newexpr[, new_col_id] != oldexpr[, old_col_id]
print(table(conflict))

sum(newexpr[, new_col_id])
sum(oldexpr[, old_col_id])

cbind(newexpr[conflict, c(1, new_col_id)],
      oldexpr[conflict, c(1, old_col_id)])

## View
library(pheatmap)
newexpr_mat <- (newexpr[, -1])
r_expressed <- which(rowSums(newexpr_mat) > 0)
r <- sample(r_expressed, 100, replace = F)
pheatmap(newexpr_mat[r, ], cluster_cols=F, cluster_rows = F,
         show_colnames=F, show_rownames=F, border_color=NA,
         filename = 'new_expr_example.png', width=7, height=7,
         main='Subset of UMI count matrix by new pipeline')
oldexpr_mat <- (oldexpr[, -1])
pheatmap(oldexpr_mat[r, ], cluster_cols=F, cluster_rows = F,
         show_colnames=F, show_rownames=F, border_color=NA,
         filename = 'old_expr_example.png', width=7, height=7,
         main='Subset of UMI count matrix by original pipeline')


## optional: check all automatically for all cells
for (i in seq(2, ncol(newexpr), 1)){
  cat('\n# Sample', i, '\n')
  new_col_id <- old_col_id <- i
  conflict <- newexpr[, new_col_id] != oldexpr[, old_col_id]
  cat('## how much confliction?\n')
  print(table(conflict))
  cat('## random 2 expressed genes\n')
  r <- sample(which(oldexpr[, i]>0), 2)
  print(cbind(oldexpr[r, c(1, old_col_id)],  newexpr[r, new_col_id]))

}



