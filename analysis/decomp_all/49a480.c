
void FUN__text__0049a480(undefined1 param_1,undefined2 param_2,undefined2 param_3,undefined4 param_4
                        )

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  undefined1 local_14 [4];
  undefined1 local_10 [4];
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__0043d4e0();
  local_c = 0;
  do {
    if (local_c == 0xfa) {
      local_8 = 0x49a5f1;
      FUN__text__0056ce80();
      return;
    }
    local_18 = local_8 + 0x80aec + local_c * 0x520;
    iVar2 = FUN__text__00468d10(local_18);
    if (iVar2 != 0) {
      iVar2 = FUN__text__0046ab20(local_18,param_1);
      if ((iVar2 != 0) && (*(char *)(*(int *)(local_18 + 600) + 0xf) == '\x01')) {
        iVar2 = FUN__text__0043d660(param_2,CONCAT22((short)((uint)*(int *)(local_18 + 600) >> 0x10)
                                                     ,param_3),param_4,
                                    *(undefined1 *)(*(int *)(local_18 + 600) + 0x30),local_10,
                                    local_14);
        if (iVar2 == 0) {
          iVar2 = FUN__text__00424f80(&DAT_0059eb90,
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlStMem.cpp",
                                      DAT_0061a06c + 0x18,0);
          if (iVar2 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
        else {
          *(undefined1 *)(*(int *)(local_18 + 600) + 0x9b) = local_10[0];
          *(undefined1 *)(*(int *)(local_18 + 600) + 0x9c) = local_14[0];
          FUN__text__00468690(local_18,*(undefined1 *)(*(int *)(local_18 + 600) + 0x9b),
                              *(undefined1 *)(*(int *)(local_18 + 600) + 0x9c));
        }
      }
    }
    local_c = local_c + 1;
  } while( true );
}

