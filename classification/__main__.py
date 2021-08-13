import argparse
import sys
from . import classifier


def main():
    """
    コマンドライン実行時のエントリーポイント
    """
    parser = argparse.ArgumentParser(
        description='classify image.', prog='classification')
    subparsers = parser.add_subparsers()
    parser_c = subparsers.add_parser('cl', help='classify image.')
    parser_c.add_argument('file', type=str, help='image file path')
    parser_c.set_defaults(func=classify)

    parser_h = subparsers.add_parser('hs', help='show classified history.')
    parser_h.set_defaults(func=history)

    if len(sys.argv) == 1:
        # 引数がない場合helpを出す
        parser.print_help()
        return

    args = parser.parse_args()
    args.func(args)


def classify(args):
    """
    分類してDBへ保存
    """
    classifier.save_classify(args.file)


def history(args):
    """
    履歴の表示
    """
    classifier.show_history()


if __name__ == '__main__':
    main()
