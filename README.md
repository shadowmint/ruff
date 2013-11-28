## Ruff

*Ruff* basically, exists to do two things:

- Watch for changes in targets.
- If there are changes in target, run build operations.

### Watches:

A watch is a set of folder patterns to observe.
If any change we can:

- immediately trigger a build
- trigger a build after at least X from last operation

Use:

    x = ruff.target()
    x.pattern('*.c', 'folder', recurse=True)
    x.pattern('*.h', 'folder', recurse=True)
    x.pattern('blah.cxx', 'folder')

### Builds:

A build operation is something that runs~

Use:

    x = ruff.target()
    x.run('

### Usage:

To use ruff you create a ruff.py somewhere, which sets all of this stuff up.

    import ruff

    scss = ruff.target()
    scss.pattern("regex", "folder", recurse=True)

    rebuild_scss = ruff.build()
    rebuild_scss.run('scss', 'blah.scss', 'output.scss')

    redeploy = ruff.build()
    redeploy.run('rsync', 'here', 'there')

    ruff.bind(scss, rebuild_scss, redeploy, timeout=10)  # Run at most every 10 seconds
    ruff.run()

### Server:

For dev purposes ruff comes with a built in webserver.

    import ruff

    ...

    run.serve('localhost', 6001, 'path_to_thing')

Never use this for anything important, obviously.

### Assets and paths:

It's often irritating to resolve paths. Ruff has a built in helper for this:

    import ruff

    # Paths
    scss_src_folder = ruff.path(__file__, 'src', 'css')
    scss_deploy_folder = ruff.path(__file__, 'app', 'static')
    scss_root = ruff.path(src_folder, 'styles.scss')
    scss_root_output = ruff.path(src_folder, 'styles.scss')

    # Deploy to server
    scss_deploy = ruff.build()
    scss_deploy.run('cp', scss_root_output, deploy_folder)

    # Watch css
    scss_target = ruff.target()
    scss_target.pattern('*.scss', src_folder, recurse=True)
    scss_target.pattern('*.css', src_folder, recurse=True)

    # run~
    ruff.bind(scss_target, scss_deploy)
    ruff.run(__file__)

### Api reference:

#### ruff

    - ruff.serve(host, port, folder)
    Set ruff to run local flask static content server for the given folder.
    NB. The server will not actually start until ruff.run() is called.

    - ruff.bind(target, build, build, build, ..., timeout=None)
    Bind a watcher to a set of build operations of arbitrary length.
    If timeout is supplied, run the build operations at most this often.

    - ruff.path(file, segment, segment, ...)
    Given the finite file 'file' (use __file__ typically) this will return
    the absolute path segment/segment/... relative to the given file.

    - ruff.run(file)
    Run ruff until it gets an interrupt signal, using dirname(file) as the
    current working context.

    - ruff.target()
    Create a ruff.Target and return it.

    - ruff.build()
    Create a ruff.Build and return it.

    - ruff.ANY
    Constant for any OS

    - ruff.WINDOWS
    Constant for windows based os

    - ruff.MAC
    Constant for mac based os

    - ruff.LINUX
    Constant for linux based os

#### ruff.Target

    - ruff.Target.pattern(regex, folder, recurse=False)
    Adds a target which triggers for any file in folder that matches the
    regex given. If recurse is set to true, the operation is recursive.

#### ruff.Build

    - ruff.Build.chdir(folder)
    Changes the current working folder. At the start of any build
    operation this is reset to the current working path.

    - ruff.Build.run(arg1, arg2, arg3..., os=ruff.ANY)
    Adds a build step that will run the arbitrary command given. 
    Ruff provides trivial detection of os and runs build commands
    only for the given platform. 
