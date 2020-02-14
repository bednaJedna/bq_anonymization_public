import helpers.functions as f


def main():
    args = f.parse_args()

    if args.random:
        f.run_random(f.TAGS)

    if args.clear:
        f.clear_json(f.PATH_CONFIG)

    if args.behave:
        f.run_all()

    if args.tags_list:
        f.run_tags(args.tags_list)


if __name__ == "__main__":
    main()
