{
  python3Packages,
  copyDesktopItems,
  makeDesktopItem,
  gobject-introspection,
  v4l-utils,
  wrapGAppsHook3,
  lib,
  ffmpeg,
}:

python3Packages.buildPythonApplication {
  pname = "camset";
  version = "0.0.21";
  pyproject = false;

  src = ./.;

  build-system = with python3Packages; [ setuptools ];

  nativeBuildInputs = [
    gobject-introspection
    wrapGAppsHook3
    copyDesktopItems
  ];

  dependencies = with python3Packages; [
    pygobject3
  ];

  dontWrapGApps = true;

  preFixup = ''
    makeWrapperArgs+=(
      "''${gappsWrapperArgs[@]}"
      --prefix PATH : ${lib.makeBinPath [ v4l-utils ffmpeg ]}
    )
  '';

  desktopItems = [
    (makeDesktopItem {
      name = "camset";
      exec = "camset";
      icon = "camera";
      comment = "Adjust webcam settings";
      desktopName = "Camset";
      categories = [
        "Utility"
        "Video"
      ];
      type = "Application";
    })
  ];

  meta = {
    description = "GUI for Video4Linux adjustments of webcams";
    homepage = "https://github.com/azeam/camset";
    license = lib.licenses.gpl3Only;
    maintainers = with lib.maintainers; [ averdow ];
  };
}
