# Six expanding review question blocks

Create these six manual containers directly in the review page content container, after `cntReviewDetails`. They display the complete current prompts and responses. Use no input controls and no fixed-line clipping. All labels use Segoe UI and wrap. Each container Fill = Theme.Surface, BorderColor = Theme.Border, BorderThickness = 1, corner radii = 8. The formula for its Height refers only to its children, not its parent Height, avoiding a layout cycle.

For the first container use X = `cntReviewDetails.X`, Width = `cntReviewDetails.Width`. Use that same X/Width for the remaining five. `cntReviewDetails` must have its explicit Height from the main review guide.

## Review slot 1

| Control / property | Value |
|---|---|
| `cntReviewQ1.Y` | `cntReviewDetails.Y+cntReviewDetails.Height+If(1<=varQuestionCount,18,0)` |
| `cntReviewQ1.Visible` | `1<=varQuestionCount` |
| `cntReviewQ1.Height` | `If(Self.Visible,lblReviewAnswer1.Y+lblReviewAnswer1.Height+24,0)` |
| `lblReviewHeading1` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 1"))` |
| `lblReviewPrompt1` | X `28`; Y `lblReviewHeading1.Y+lblReviewHeading1.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=1,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer1` | X `28`; Y `lblReviewPrompt1.Y+lblReviewPrompt1.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=1,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

## Review slot 2

| Control / property | Value |
|---|---|
| `cntReviewQ2.Y` | `cntReviewQ1.Y+cntReviewQ1.Height+If(2<=varQuestionCount,18,0)` |
| `cntReviewQ2.Visible` | `2<=varQuestionCount` |
| `cntReviewQ2.Height` | `If(Self.Visible,lblReviewAnswer2.Y+lblReviewAnswer2.Height+24,0)` |
| `lblReviewHeading2` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 2"))` |
| `lblReviewPrompt2` | X `28`; Y `lblReviewHeading2.Y+lblReviewHeading2.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=2,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer2` | X `28`; Y `lblReviewPrompt2.Y+lblReviewPrompt2.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=2,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

## Review slot 3

| Control / property | Value |
|---|---|
| `cntReviewQ3.Y` | `cntReviewQ2.Y+cntReviewQ2.Height+If(3<=varQuestionCount,18,0)` |
| `cntReviewQ3.Visible` | `3<=varQuestionCount` |
| `cntReviewQ3.Height` | `If(Self.Visible,lblReviewAnswer3.Y+lblReviewAnswer3.Height+24,0)` |
| `lblReviewHeading3` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 3"))` |
| `lblReviewPrompt3` | X `28`; Y `lblReviewHeading3.Y+lblReviewHeading3.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=3,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer3` | X `28`; Y `lblReviewPrompt3.Y+lblReviewPrompt3.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=3,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

## Review slot 4

| Control / property | Value |
|---|---|
| `cntReviewQ4.Y` | `cntReviewQ3.Y+cntReviewQ3.Height+If(4<=varQuestionCount,18,0)` |
| `cntReviewQ4.Visible` | `4<=varQuestionCount` |
| `cntReviewQ4.Height` | `If(Self.Visible,lblReviewAnswer4.Y+lblReviewAnswer4.Height+24,0)` |
| `lblReviewHeading4` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 4"))` |
| `lblReviewPrompt4` | X `28`; Y `lblReviewHeading4.Y+lblReviewHeading4.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=4,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer4` | X `28`; Y `lblReviewPrompt4.Y+lblReviewPrompt4.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=4,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

## Review slot 5

| Control / property | Value |
|---|---|
| `cntReviewQ5.Y` | `cntReviewQ4.Y+cntReviewQ4.Height+If(5<=varQuestionCount,18,0)` |
| `cntReviewQ5.Visible` | `5<=varQuestionCount` |
| `cntReviewQ5.Height` | `If(Self.Visible,lblReviewAnswer5.Y+lblReviewAnswer5.Height+24,0)` |
| `lblReviewHeading5` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 5"))` |
| `lblReviewPrompt5` | X `28`; Y `lblReviewHeading5.Y+lblReviewHeading5.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=5,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer5` | X `28`; Y `lblReviewPrompt5.Y+lblReviewPrompt5.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=5,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

## Review slot 6

| Control / property | Value |
|---|---|
| `cntReviewQ6.Y` | `cntReviewQ5.Y+cntReviewQ5.Height+If(6<=varQuestionCount,18,0)` |
| `cntReviewQ6.Visible` | `6<=varQuestionCount` |
| `cntReviewQ6.Height` | `If(Self.Visible,lblReviewAnswer6.Y+lblReviewAnswer6.Height+24,0)` |
| `lblReviewHeading6` | X `28`; Y `24`; Width `Parent.Width-56`; AutoHeight `true`; Size `12.75`; Semibold; Color `Theme.Heading` |
| Heading Text | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,First(Split(p,Char(10))).Value,"Criterion 6"))` |
| `lblReviewPrompt6` | X `28`; Y `lblReviewHeading6.Y+lblReviewHeading6.Height+10`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Muted` |
| Prompt Text | `With({p:LookUp(colAnswers,Slot=6,Prompt)},If(Char(10) in p,Mid(p,Find(Char(10),p)+1),p))` |
| `lblReviewAnswer6` | X `28`; Y `lblReviewPrompt6.Y+lblReviewPrompt6.Height+16`; Width `Parent.Width-56`; AutoHeight `true`; Size `9.75`; Color `Theme.Body` |
| Answer Text | `With({a:LookUp(colAnswers,Slot=6,Response)},If(IsBlank(Trim(a)),"No response supplied (optional).",a))` |

Place `cntReviewEvidence.Y` at `cntReviewQ6.Y+cntReviewQ6.Height+18`. Hidden trailing question containers have zero Height and add no gap.
