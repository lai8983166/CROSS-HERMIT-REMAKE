
void __fastcall FUN__text__00456650(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  char local_14;
  char *local_10;
  undefined1 local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = (char *)(*(int *)(param_1 + 0x60) + 0x2434);
  if (*local_10 != '\0') {
    local_8 = param_1;
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_8 + 0x148) = 8;
    local_14 = local_10[1];
    if (local_14 == '\0') {
      FUN__text__00407870((int)*(short *)(&DAT_0060cb04 + *(short *)(local_10 + 4) * 4),
                          (int)*(short *)(&PTR_DAT_0060cb06 + *(short *)(local_10 + 4)));
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                  DAT_0060cdb8 + 0x15,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    *(undefined4 *)(local_8 + 0x14c) = 1;
    *(undefined2 *)(local_8 + 0x166) = *(undefined2 *)(local_10 + 0x10);
    local_c = (undefined1)((uint)*(undefined4 *)(local_10 + 0x14) >> 8);
    *(undefined1 *)(local_8 + 0x157) = local_c;
    *(undefined1 *)(local_8 + 0x154) = 0x80;
    *(undefined1 *)(local_8 + 0x155) = 0x80;
    *(undefined1 *)(local_8 + 0x156) = 0x80;
    FUN__text__004079c0((int)*(short *)(local_10 + 8) + (int)*(short *)(local_10 + 0xc),
                        (int)*(short *)(local_10 + 10) + (int)*(short *)(local_10 + 0xe));
  }
  local_8 = 0x4567ab;
  FUN__text__0056ce80();
  return;
}

