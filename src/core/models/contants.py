class CONSTANTS:
    class ROLE:
        admin = 'admin'
        seller = 'seller'

        CHOICES = (
            (admin, 'Admin'),
            (seller, 'Seller'),
        )

    class PAYMENT_TYPE:
        debt = 'debt'
        payment = 'payment'

        CHOICES = (
            (debt, 'Qarz'),
            (payment, 'To\'lov'),
        )

    class DOC_PURCHASE_STATUS:
        pending = 'pending'
        completed = 'completed'

        CHOICES = (
            (pending, "Kutilmoqda"),
            (completed, "Sotib olindi"),
        )

    class DOC_PURCHASE_RETURN_REASON:
        defective = 'defective'

        CHOICES = (
            (defective, 'Nuqsonli'),
        )

    class DOC_ORDER_PAYMENT_STATUS:
        paid = 'paid'
        partial_paid = 'partial_paid'
        debt = 'debt'
        overdue = 'overdue'

        CHOICES = (
            (paid, "To'langan"),
            (partial_paid, "Qisman to'langan"),
            (debt, "Qarzga olingan"),
            (overdue, "Muddati o'tkan"),
        )

    class DOC_ORDER_PAYMENT_METHOD:
        cash = 'cash'
        card = 'card'

        CHOICES = (
            (cash, 'Naqt pul'),
            (card, 'Plastik karta'),
        )

    class DOC_ORDER_STATUS:
        pending = 'pending'
        completed = 'completed'

        CHOICES = (
            (pending, "Kutilmoqda"),
            (completed, "Sotildi"),
        )

    class DOC_ORDER_RETURN_STATUS:
        pending = 'pending'
        completed = 'completed'

        CHOICES = (
            (pending, "Kutilmoqda"),
            (completed, "Qaytarildi"),
        )
