
## Manually Check Consistency
#
# Adapt to your system
# library(readr)
# celseq2 <- read_csv("celseq2_demo.csv")
# expression_1M <- read_delim("expression_1M.tab",
#                             "\t", escape_double = FALSE,
#                             trim_ws = TRUE)

newexpr <- celseq2
oldexpr <- expression_1M[1:nrow(newexpr), ] ## tail several lines unwanted

## whether rownames are consistent
rownames_newexpr <- unlist(c(newexpr[, 1]))
rownames_oldexpr <- unlist(c(oldexpr[, 1]))
table(rownames_newexpr == rownames_oldexpr)

## Make sure cells are same before checking values
new_col_id <- 7
old_col_id <- 7
print(colnames(newexpr)[new_col_id])
print(colnames(oldexpr)[old_col_id])

## test whether genes have different UMI counts
conflict <- newexpr[, new_col_id] != oldexpr[, old_col_id]
table(conflict)
cbind(newexpr[conflict, c(1, new_col_id)],
      oldexpr[conflict, c(1, old_col_id)])

sum(newexpr[, new_col_id])
sum(oldexpr[, old_col_id])

