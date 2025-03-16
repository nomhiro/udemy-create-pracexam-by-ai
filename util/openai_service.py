import os
import openai
from util.model import PracticeTestItem, UdemyPracticeTestItem, JudgeResultItem

# 環境変数からAPIキーとエンドポイントを取得
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-12-01-preview"


def create_explanation_practice_test_item(item: PracticeTestItem) -> PracticeTestItem:
    prompt = f'''
    あなたはITの高度情報技術者「プロジェクトマネジメント」試験を作る高度な専門家として詳細解説を追加するように振る舞います。
    入力として与えられる資格試験の問題をもとに、日本語で各選択肢が正解の理由と間違いの理由を詳細に解説してください。
    翻訳時には以下のルールを厳守してください。

    1. 情報を改変しない
    原文の意味・意図を変えず、正確に翻訳してください。
    原文中の専門用語や固有名詞（製品名やサービス名など）は、必要に応じてそのまま使用してください。

    3. 文体と表現
    専門的かつ明瞭な日本語を用い、問題文として自然に読めるように翻訳してください。
    不要にカジュアルな表現は避け、必要があれば丁寧な敬体または常体で統一してください。

    4. 構造表現
    表形式の解説で表現する必要がある場合は、Markdownの表形式を使用してください。
    ただし、CSV出力の構造は維持しなければなりません。

    5. question_typeはそのままにしてください。

    これらのルールを遵守し、各選択肢に対する詳細解説を追加してください。

    以下は適切な翻訳の例です。
    [入力]
    {{
      "question": "PMBOKのリスクマネジメントでは、定性的リスク分析でリスク対応計画の優先順位を設定し、定量的リスク分析で数値によるリスクの等級付けを行う。定性的リスク分析で使用されるものはどれか？",
      "question_type": "multiple-choice",
      "answer_option1": "感情分析",
      "answer_option2": "期待金額価値分析",
      "answer_option3": "デシジョンツリー分析",
      "answer_option4": "発生確率・影響度マトリックス",
      "correct_answers": "4",
      "overall_explanation": "定性的リスク分析では、発生確率・影響度マトリックスを使用してリスクの優先順位を設定します。"
    }}
    [出力]
    {{
      "question": "PMBOKのリスクマネジメントでは、定性的リスク分析でリスク対応計画の優先順位を設定し、定量的リスク分析で数値によるリスクの等級付けを行う。定性的リスク分析で使用されるものはどれか？",
      "question_type": "multiple-choice",
      "answer_option1": "感情分析",
      "explanation1": "感情分析は、主に人々の感情や意見を抽出して分類するためのツールであり、マーケティングやソーシャルメディア分析に使用されます。プロジェクトマネジメントにおけるリスクの優先順位付けには適していません。",
      "answer_option2": "期待金額価値分析",
      "explanation2": "EMV（期待金額価値分析）は、リスクの発生確率と影響を金額で表現する定量的分析手法です。この手法は、リスクの財務的影響を評価し、意思決定に役立つ結果を提供しますが、定性的リスク分析の手法ではありません。",
      "answer_option3": "デシジョンツリー分析",
      "explanation3": "デシジョンツリー分析は、複数の選択肢とその結果を視覚的に表現し、定量的リスク分析や意思決定プロセスで使用されます。特定の選択肢のリスクや利益を数値化して評価するためのツールです。",
      "answer_option4": "発生確率・影響度マトリックス",
      "explanation4": "発生確率・影響度マトリックスは、定性的リスク分析で最も広く使用される手法です。各リスクの発生確率（可能性）と影響度（重要性）を評価し、その結果を2次元マトリックスにプロットします。この手法により、リスクの優先順位を視覚的かつ効率的に設定することができます。",
      "answer_option5": "",
      "explanation5": "",
      "answer_option6": "",
      "explanation6": "",
      "correct_answers": "4",
      "overall_explanation": "定性的リスク分析は、数値的な評価に基づく定量的リスク分析とは異なり、各リスクの発生確率と影響度を評価し、リスク対応計画の優先順位を設定するプロセスです。このプロセスでは、発生確率・影響度マトリックスを使用して、リスクの可視化と効率的なリスク管理が可能になります。これにより、プロジェクトマネージャーは、最も重要なリスクに集中して対応することができます。",
      "domain": "プロジェクトマネジメント"
    }}'''

    user_message = f"""
    {{
      "question": "{item.question}",
      "question_type": "{item.question_type}",
      "answer_option1": "{item.answer_option1}",
      "answer_option2": "{item.answer_option2}",
      "answer_option3": "{item.answer_option3}",
      "answer_option4": "{item.answer_option4}",
      "answer_option5": "{item.answer_option5}",
      "answer_option6": "{item.answer_option6}",
      "correct_answers": "{item.correct_answers}",
      "overall_explanation": "{item.overall_explanation}",
    }}
    """

    response = openai.beta.chat.completions.parse(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        response_format=UdemyPracticeTestItem
    )

    translated_item = response.choices[0].message.parsed
    return translated_item


def judge_practice_test_item(origin, translation_result) -> JudgeResultItem:
    prompt = f"""
    あなたはMicrosoftおよびAzure分野の技術用語に詳しい校正担当者です。
    Azureに関する資格試験の問題文を日本語に翻訳した結果を評価します。
    入力には、元の英語の問題文と、その翻訳結果が構造化された形式で与えられます。
    あなたは翻訳が正確であり、適切な日本語表現が用いられているかを評価します。
    翻訳結果が適切である場合は'ok'とだけ返します。
    翻訳結果を修正する必要がある場合は'ng'として、修正箇所を簡潔に指摘してください。

    以下は入出力の例です。
    [入力例:okの場合]
    - origin
    {{
      "question": "As the lead cloud administrator for GetCloudSkills, you have recently hired a new employee responsible for Azure AD support issues. The new employee should be able to reset passwords for all types of users, including those with user admin, global admin, or password admin roles. However, you must ensure that you follow the principle of least privilege when granting access. Which role should you grant to the new employee?",
      "question_type": "multiple-choice",
      "answer_option1": "Password Admin",
      "explanation1": "",
      "answer_option2": "Global Admin",
      "explanation2": "",
      "answer_option3": "Security Admin",
      "explanation3": "",
      "answer_option4": "User Admin",
      "explanation4": "",
      "answer_option5": "",
      "explanation5": "",
      "answer_option6": "",
      "explanation6": "",
      "correct_answers": "2",
      "overall_explanation": "Answer A is incorrect because the Password Admin role does not provide the authority to reset passwords for User Admins or Global Admins. Answer B is the correct option, as the Global Admin role would enable the new employee to reset passwords for all users.Answer C is incorrect because the Security Admin role only controls access to and configuration of Microsoft Defender for Cloud.Answer D is not the correct answer as the user admin role would not allow the new employee to reset passwords for Global Admins.If you want to learn more, go to:<a href='https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator'>Microsoft Entra built-in roles - Microsoft Entra ID | Microsoft Learn</a><a href='https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles'\\>Azure built-in roles - Azure RBAC | Microsoft Learn</a>"
      "domain": "Implement and manage user identities",
    }}
    - translation
    {{
      "question": "あなたは「GetCloudSkills」のリードクラウド管理者として、最近Azure ADのサポート業務を担当する新しい従業員を雇いました。この従業員は、ユーザー管理者、グローバル管理者、パスワード管理者のロールを持つユーザーを含む、すべてのユーザーのパスワードをリセットできる必要があります。ただし、アクセスを付与する際には最小権限の原則に従う必要があります。この従業員には、どのロールを付与すべきでしょうか？",
      "question_type": "multiple-choice",
      "answer_option1": "パスワード管理者",
      "explanation1": "",
      "answer_option2": "グローバル管理者",
      "explanation2": "",
      "answer_option3": "セキュリティ管理者",
      "explanation3": "",
      "answer_option4": "ユーザー管理者",
      "explanation4": "",
      "answer_option5": "",
      "explanation5": "",
      "answer_option6": "",
      "explanation6": "",
      "correct_answers": "2",
      "overall_explanation": "回答Aは不正解です。パスワード管理者ロールには、ユーザー管理者やグローバル管理者のパスワードをリセットする権限がありません。回答Bが正解です。グローバル管理者ロールを付与することで、新しい従業員はすべてのユーザーのパスワードをリセットできるようになります。回答Cは不正解です。セキュリティ管理者ロールは、Microsoft Defender for Cloud のアクセス制御や構成を管理するためのものであり、パスワードリセットの権限は含まれていません。回答Dは不正解です。ユーザー管理者ロールでは、新しい従業員がグローバル管理者のパスワードをリセットすることはできません。詳細については、以下のリンクをご参照ください：<a href='https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#user-administrator'>Microsoft Entra built-in roles - Microsoft Entra ID | Microsoft Learn</a><a href='https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles'\\>Azure built-in roles - Azure RBAC | Microsoft Learn</a>",
      "domain": "ユーザーIDの実装と管理",
    }}
    [出力例:okの場合]
    {{
      "result": "ok",
      "comment": ""
    }}

    [入力例:ngの場合]
    - origin
    {{
      'question': 'As an Azure Administrator for your organization, you are responsible for creating multiple security groups and assigning users to them based on specific profile attributes. The process should be automated so that new users are automatically added to the appropriate group when they join the organization. What type of group should you configure?',
      'question_type': 'multiple-choice',
      'answer_option1': 'Power Group',
      'explanation1': '',
      'answer_option2': 'Smart Group',
      'explanation2': '',
      'answer_option3': 'Microsoft 365 Group',
      'explanation3': '',
      'answer_option4': 'Dynamic Group',
      'explanation4': '',
      'answer_option5': '',
      'explanation5': '',
      'answer_option6': '',
      'explanation6': '',
      'correct_answers': '4',
      'overall_explanation': "Answer A is not correct because Power Groups is not a valid setting in Azure Active Directory. Answer B is also incorrect because Smart Groups is not a valid setting in Azure Active Directory. Answer C is not correct as Microsoft 365 groups is a valid group type in Azure Active Directory. Still, it does not provide the ability to automatically add users to groups based on profile attributes. Answer D, on the other hand, is correct. Dynamic groups allow administrators to set rules to populate groups created in Azure AD based on user attributes such as user type, department, or country/region.If you want to learn more, go to:<a href='https://learn.microsoft.com/en-us/entra/external-id/use-dynamic-groups'>Dynamic groups and B2B collaboration - Microsoft Entra External ID | Microsoft Learn</a>",
      'domain': 'Implement and manage user identities'
    }}
    - translation
    {{
      'question': 'あなたは組織のAzure管理者として、特定のプロファイル属性に基づいて複数のセキュリティグループを作成し、ユーザーをそれらに割り当てる責任があります。新しいユーザーが組織に参加すると、適切なグループに自動的に追加されるようにプロセスを自動化する必要があります。どのタイプのグループを構成する必要がありますか？',
      'question_type': 'multiple-choice',
      'answer_option1': 'パワーグループ',
      'explanation1': '',
      'answer_option2': 'スマートグループ',
      'explanation2': '',
      'answer_option3': 'Microsoft 365 グループ',
      'explanation3': '',
      'answer_option4': 'ダイナミックグループ',
      'explanation4': '',
      'answer_option5': '',
      'explanation5': '',
      'answer_option6': '',
      'explanation6': '',
      'correct_answers': '4',
      'overall_explanation': "回答Aは不正解です。パワーグループはAzure Active Directoryで有効な設定ではありません。回答Bも不正解です。スマートグループはAzure Active Directoryで有効な設定ではありません。回答Cも不正解です。Microsoft 365 グループはAzure Active Directoryで有効なグループタイプですが、プロファイル属性に基づいてユーザーを自動的にグループに追加する機能は提供していません。一方、回答Dは正解です。ダイナミックグループを使用すると、Azure ADで作成されたグループにユーザーの属性（ユーザータイプ、部署、国/地域など）に基づいてルールを設定してグループを自動的に割り当てることができます。詳細については、以下のリンクをご参照ください：<a href='https://learn.microsoft.com/en-us/entra/external-id/use-dynamic-groups'>Dynamic groups and B2B collaboration - Microsoft Entra External ID | Microsoft Learn</a>",
      'domain': 'ユーザーIDの実装と管理'
    }}

    [出力:ngの場合]
    {{
      "result": "ng",
      "comment": "「ダイナミックグループ」は日本語に翻訳する際に、原文の意味を正確に表現していません。原文の「Dynamic Group」は、Azure Active Directoryでユーザー属性に基づいてグループを自動的に作成する機能を指しています。したがって、適切な翻訳は「動的グループ」です。"
    }}
    """

    user_message = f"""
    - origin
    {origin}
    - translation
    {translation_result}
    """

    response = openai.beta.chat.completions.parse(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        response_format=JudgeResultItem
    )

    judge_result = response.choices[0].message.parsed
    return judge_result
