from storage.storage import Storage
import argparse


def main(command, args):
    storage = Storage()

    if command.lower() == "loginaws":
        storage.login()

    if command.lower() == "listobjects":
        storage.list_objects_by_bucket_name(args.bucket)

    if command.lower() == "putobject":
        if args.bucket and args.filepath:
            storage.put_object(args.bucket, args.filepath)

        else:
            print("No bucket name or filepath provided")

    if command.lower() == "deleteobject":
        if args.bucket and args.filepath:
            storage.delete_object(args.bucket, args.filepath)

        else:
            print("No bucket name or filepath provided")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Storage CLI')

    subparsers = parser.add_subparsers(dest='command')
    login_aws = subparsers.add_parser('Loginaws')
    list_objects = subparsers.add_parser('ListObjects')
    put_object = subparsers.add_parser('PutObject')
    delete_object = subparsers.add_parser('DeleteObject')


    login_aws.add_argument('--bucket',
                              help='Bucket Name of the Bucket to print - Optional',
                              default=None)
    list_objects.add_argument('--bucket',
                              help='Bucket Name of the Bucket to print - Optional',
                              default=None)
    put_object.add_argument('--bucket',
                            help='Bucket Name of the Bucket to use')
    put_object.add_argument('--filepath',
                            help='Local file path of the file to use')
    delete_object.add_argument('--bucket',
                               help='Bucket Name of the Bucket to use')
    delete_object.add_argument('--filepath',
                               help='Local file path of the file to use')
    args = parser.parse_args()

    main(args.command, args)
