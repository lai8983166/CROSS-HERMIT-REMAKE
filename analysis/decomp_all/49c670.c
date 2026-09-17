
void FUN__text__0049c670(undefined2 param_1,undefined2 param_2)

{
  ushort uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  ushort local_10;
  undefined2 uStack_e;
  int local_c;
  int local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = FUN__text__00470070(0x18c,600,0x18e,0xa8,param_1,CONCAT22(0xcccc,param_2));
  if (iVar3 != 0) {
    for (local_c = 0; local_c != 0x14; local_c = local_c + 1) {
      iVar3 = FUN__text__00470070(CONCAT22((short)((uint)local_c >> 0x10),
                                           (&DAT_0061adb8)[local_c * 4]),
                                  (&DAT_0061adbc)[local_c * 4],0x24,0x24,param_1,param_2);
      if (iVar3 != 0) {
        if ((3 < local_c) && (local_c < 0xc)) {
          if (*(int *)(local_8 + 0x108b50) != 0) {
            uVar1 = *(ushort *)(*(int *)(*(int *)(local_8 + 0x108b60) + 600) + 0x7c + local_c * 2);
            _local_10 = CONCAT22(uStack_e,uVar1);
            uVar2 = _local_10;
            if (((uVar1 & 0x8000) == 0) && (uVar1 != 0)) {
              *(undefined1 *)(local_8 + 0x2f15c) = 2;
              local_10._0_1_ = (undefined1)uVar1;
              *(undefined1 *)(local_8 + 0x2f15e) = (undefined1)local_10;
              _local_10 = uVar2;
              break;
            }
          }
          *(undefined1 *)(local_8 + 0x2f15c) = 0xff;
          *(undefined1 *)(local_8 + 0x2f15e) = 0xff;
          break;
        }
        if (local_c == 0) {
          if (((*(int *)(local_8 + 0x108b50) == 0) ||
              (iVar3 = FUN__text__0046a430(*(undefined4 *)(local_8 + 0x108b60)), iVar3 == 0)) ||
             (*(char *)(*(int *)(*(int *)(local_8 + 0x108b60) + 600) + 0x9d) == '\0')) {
            *(undefined1 *)(local_8 + 0x2f15e) = 0;
          }
          else {
            *(undefined1 *)(local_8 + 0x2f15e) = 0x14;
          }
        }
        else {
          *(undefined1 *)(local_8 + 0x2f15e) = (undefined1)local_c;
        }
        *(undefined1 *)(local_8 + 0x2f15c) = 1;
        break;
      }
    }
  }
  local_8 = 0x49c849;
  FUN__text__0056ce80();
  return;
}

