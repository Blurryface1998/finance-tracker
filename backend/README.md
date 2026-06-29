Need to learn list comprehensions for this part:
def get_category_summary_service(db: Session):
query = db.query(Transaction.category, func.sum(Transaction.amount)).group_by(Transaction.category)

    # List comprehensions
    result = []

    for category, total in query:
        result.append(CategorySummary(category=category, total=total))

    return result
