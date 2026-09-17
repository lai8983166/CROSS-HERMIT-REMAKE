
void FUN__text__0044f460(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [20];
  int local_10;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_2 + 0x1e) = 0;
  *(undefined2 *)(param_2 + 0x20) = 0;
  if (*(int *)(param_1 + 0x14) == 0) {
    *(undefined1 *)(param_2 + 0x22) = *(undefined1 *)(param_1 + 2);
    *(undefined1 *)(param_2 + 0x23) = *(undefined1 *)(param_1 + 4);
    *(undefined1 *)(param_2 + 0x24) = *(undefined1 *)(param_2 + 0x18);
    *(undefined1 *)(param_2 + 0x25) = *(undefined1 *)(param_2 + 0x1a);
    *(undefined2 *)(param_2 + 0x1e) = 0;
    *(undefined2 *)(param_2 + 0x20) = 2;
  }
  else {
    local_10 = param_1;
    *(undefined4 *)(param_1 + 0x18) = 0;
    do {
      iVar1 = *(int *)(local_10 + 0x14);
      *(int *)(iVar1 + 0x18) = local_10;
      local_10 = iVar1;
    } while (*(int *)(iVar1 + 0x14) != 0);
    iVar1 = *(int *)(iVar1 + 0x18);
    if (*(int *)(iVar1 + 0x18) == 0) {
      *(undefined1 *)(param_2 + 0x22 + *(short *)(param_2 + 0x20) * 2) = *(undefined1 *)(iVar1 + 2);
      *(undefined1 *)(param_2 + 0x23 + *(short *)(param_2 + 0x20) * 2) = *(undefined1 *)(iVar1 + 4);
      *(short *)(param_2 + 0x20) = *(short *)(param_2 + 0x20) + 1;
      *(undefined1 *)(param_2 + 0x22 + *(short *)(param_2 + 0x20) * 2) =
           *(undefined1 *)(param_2 + 0x18);
      *(undefined1 *)(param_2 + 0x23 + *(short *)(param_2 + 0x20) * 2) =
           *(undefined1 *)(param_2 + 0x1a);
      *(short *)(param_2 + 0x20) = *(short *)(param_2 + 0x20) + 1;
    }
    else {
      do {
        *(undefined1 *)(param_2 + 0x22 + *(short *)(param_2 + 0x20) * 2) =
             *(undefined1 *)(local_10 + 2);
        *(undefined1 *)(param_2 + 0x23 + *(short *)(param_2 + 0x20) * 2) =
             *(undefined1 *)(local_10 + 4);
        *(short *)(param_2 + 0x20) = *(short *)(param_2 + 0x20) + 1;
        local_10 = *(int *)(local_10 + 0x18);
        if (local_10 == 0) {
          *(undefined1 *)(param_2 + 0x22 + *(short *)(param_2 + 0x20) * 2) =
               *(undefined1 *)(param_2 + 0x18);
          *(undefined1 *)(param_2 + 0x23 + *(short *)(param_2 + 0x20) * 2) =
               *(undefined1 *)(param_2 + 0x1a);
          *(short *)(param_2 + 0x20) = *(short *)(param_2 + 0x20) + 1;
          return;
        }
      } while (*(short *)(param_2 + 0x20) < 100);
    }
  }
  return;
}

