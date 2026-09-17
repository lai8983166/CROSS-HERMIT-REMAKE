
uint FUN__text__0048a730(int param_1,int param_2,int param_3,ushort *param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  uint local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(*(undefined1 *)(param_1 + 5)) {
  case 0:
    local_c = (uint)*param_4;
    break;
  case 1:
    local_c = (uint)*param_4;
    break;
  case 2:
    local_c = (uint)param_4[1] + (int)*(short *)(param_2 + 0x24) +
              (int)((uint)*(byte *)(*(int *)(param_3 + 600) + 4) * (int)*(short *)(param_2 + 0x26))
              / 100;
    break;
  case 3:
    local_c = (int)*(short *)(param_2 + 0x24) +
              (int)((uint)*(byte *)(*(int *)(param_3 + 600) + 4) * (int)*(short *)(param_2 + 0x26))
              / 100;
    break;
  case 4:
    local_c = (uint)param_4[1] + (int)*(short *)(param_2 + 0x24) +
              (int)((uint)*(byte *)(*(int *)(param_3 + 600) + 5) * (int)*(short *)(param_2 + 0x26))
              / 100;
    break;
  case 5:
    local_c = (uint)param_4[1] + (int)*(short *)(param_2 + 0x24) +
              (int)((uint)*(byte *)(*(int *)(param_3 + 600) + 6) * (int)*(short *)(param_2 + 0x26))
              / 100;
    break;
  case 6:
    local_c = (int)*(short *)(param_2 + 0x24) +
              (int)((uint)*(byte *)(*(int *)(param_3 + 600) + 6) * (int)*(short *)(param_2 + 0x26))
              / 100;
    break;
  case 7:
    local_c = (int)*(short *)(param_2 + 0x24) +
              (int)((uint)*(byte *)(*(int *)(param_3 + 600) + 7) * (int)*(short *)(param_2 + 0x26))
              / 100;
    break;
  case 8:
    local_c = (int)*(short *)(param_2 + 0x24) +
              (int)((uint)*(byte *)(*(int *)(param_3 + 600) + 8) * (int)*(short *)(param_2 + 0x26))
              / 100;
    break;
  case 9:
    local_c = (((int)((uint)*(byte *)(*(int *)(param_3 + 600) + 8) *
                     ((uint)*(byte *)(*(int *)(param_3 + 600) + 8) +
                      (uint)*(byte *)(*(int *)(param_3 + 600) + 9) + (int)*(short *)(param_2 + 0x24)
                     )) / 100) * (int)*(short *)(param_2 + 0x26)) / 100;
    break;
  case 10:
    local_c = (((int)(((uint)*(byte *)(*(int *)(param_3 + 600) + 8) +
                       (uint)*(byte *)(*(int *)(param_3 + 600) + 5) +
                      (int)*(short *)(param_2 + 0x24)) *
                     (uint)*(byte *)(*(int *)(param_3 + 600) + 8)) / 100) *
              (int)*(short *)(param_2 + 0x26)) / 100;
    break;
  case 0xb:
    local_c = (((int)(((uint)*(byte *)(*(int *)(param_3 + 600) + 8) +
                       (uint)*(byte *)(*(int *)(param_3 + 600) + 7) +
                      (int)*(short *)(param_2 + 0x24)) *
                     (uint)*(byte *)(*(int *)(param_3 + 600) + 8)) / 100) *
              (int)*(short *)(param_2 + 0x26)) / 100;
    break;
  case 0xc:
    local_c = (((int)(((uint)*(byte *)(*(int *)(param_3 + 600) + 8) +
                       (uint)*(byte *)(*(int *)(param_3 + 600) + 4) +
                      (int)*(short *)(param_2 + 0x24)) *
                     (uint)*(byte *)(*(int *)(param_3 + 600) + 8)) / 100) *
              (int)*(short *)(param_2 + 0x26)) / 100;
  }
  param_4[1] = (ushort)local_c;
  return local_c;
}

