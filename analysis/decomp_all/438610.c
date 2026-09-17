
void __thiscall FUN__text__00438610(undefined4 param_1,int param_2,int param_3,undefined4 param_4)

{
  int iVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  undefined2 local_1c;
  undefined2 local_18;
  int local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(undefined2 *)(param_3 + 0x1e) = 0;
  *(undefined2 *)(param_3 + 0x20) = 0;
  if (*(int *)(param_2 + 0x14) == 0) {
    *(undefined2 *)(param_3 + 0x1e) = 0;
    *(undefined2 *)(param_3 + 0x20) = 0;
  }
  else {
    local_10 = param_2;
    *(undefined4 *)(param_2 + 0x18) = 0;
    do {
      iVar1 = *(int *)(local_10 + 0x14);
      *(int *)(iVar1 + 0x18) = local_10;
      local_10 = iVar1;
    } while (*(int *)(iVar1 + 0x14) != 0);
    local_c = *(int *)(iVar1 + 0x18);
    local_8 = param_1;
    if (*(int *)(local_c + 0x18) == 0) {
      *(undefined1 *)(param_3 + 0x22 + *(short *)(param_3 + 0x20) * 2) =
           *(undefined1 *)(local_c + 2);
      *(undefined1 *)(param_3 + 0x23 + *(short *)(param_3 + 0x20) * 2) =
           *(undefined1 *)(local_c + 4);
      *(short *)(param_3 + 0x20) = *(short *)(param_3 + 0x20) + 1;
    }
    else {
      do {
        local_18 = *(undefined2 *)(local_10 + 2);
        local_1c = *(undefined2 *)(local_10 + 4);
        local_14 = *(int *)(local_10 + 0x18);
        local_c = local_14;
        while (uVar2 = (undefined2)((uint)local_c >> 0x10),
              iVar1 = FUN__text__004388e0(CONCAT22(uVar2,local_18),local_1c,
                                          CONCAT22(uVar2,*(undefined2 *)(local_c + 2)),
                                          *(undefined2 *)(local_c + 4),param_4), iVar1 != 0) {
          if (*(int *)(local_c + 0x18) == 0) {
            local_14 = local_c;
            break;
          }
          local_14 = local_c;
          local_c = *(int *)(local_c + 0x18);
        }
        local_10 = local_14;
        *(undefined1 *)(param_3 + 0x22 + *(short *)(param_3 + 0x20) * 2) =
             *(undefined1 *)(local_14 + 2);
        *(undefined1 *)(param_3 + 0x23 + *(short *)(param_3 + 0x20) * 2) =
             *(undefined1 *)(local_14 + 4);
        *(short *)(param_3 + 0x20) = *(short *)(param_3 + 0x20) + 1;
      } while ((*(int *)(local_14 + 0x18) != 0) && (*(short *)(param_3 + 0x20) < 100));
    }
  }
  local_8 = 0x4387e2;
  FUN__text__0056ce80();
  return;
}

